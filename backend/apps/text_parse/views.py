import logging
import redis
import json
import uuid
import os.path as op
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.http.response import (
    JsonResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from .tasks import parse_file


log = logging.getLogger('app.text_parse')
r = redis.Redis.from_url(url=settings.REDIS_URL)

REDIS_NAME_PREFIX = 'parse_file_result_'


def get_redis_name(hs):
    return REDIS_NAME_PREFIX + hs


def get_parse_results(hs):
    redis_name = get_redis_name(hs)
    values = r.get(redis_name)
    return json.loads(values)


class XhrView(View):
    response_class = JsonResponse

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden(content=b'Ajax request only.')
        action_name = kwargs.get('action_name', '')
        if action_name.startswith('_'):
            return HttpResponseBadRequest(content=b'Action not knowing.')
        action = getattr(self, action_name.lower(), None)
        if not callable(action):
            return HttpResponseNotFound(content='Action not found.')
        return self.response_class(action(request))

    def upload(self, request):
        file = request.FILES['file']
        hs = uuid.uuid4().hex
        _, ext = op.splitext(file.name)
        dest_path = op.join(settings.UPLOAD_DIR, hs + ext)
        with open(dest_path, 'w+b') as f:
            for chunk in file.chunks():
                f.write(chunk)
        redis_name = get_redis_name(hs)
        parse_file.delay(dest_path, file.name, redis_name)
        return {
            'result': 'OK',
            'result_hash': hs,
            'next': reverse('parse', kwargs={'hash': hs}),
        }

    def parse_results(self, request):
        hash = request.GET.get('hash', '')
        if not hash:
            return {}
        return get_parse_results(hash)


class IndexView(TemplateView):
    template_name = 'text_parse/index.html'


class ParseView(TemplateView):
    template_name = 'text_parse/parse.html'

    def get_context_data(self, **kwargs):
        kwargs.update(super().get_context_data(**kwargs))
        hs = kwargs.get('hash', None)
        if hs:
            kwargs['result'] = get_parse_results(hs)
        return kwargs
