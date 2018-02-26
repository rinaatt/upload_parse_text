import logging
import redis
import uuid
import os.path as op
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.http.response import JsonResponse
from .tasks import parse_file


log = logging.getLogger('app.text_parse')
r = redis.Redis.from_url(url=settings.REDIS_URL)


class IndexView(TemplateView):
    template_name = 'text_parse/index.html'


class UploadView(View):

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        hs = uuid.uuid4().hex
        _, ext = op.splitext(file.name)
        dest_path = op.join(settings.UPLOAD_DIR, hs+ext)
        with open(dest_path, 'w+b') as f:
            for chunk in file.chunks():
                f.write(chunk)
        redis_name = 'parse_file_result_' + hs
        parse_file.delay(dest_path, file.name, redis_name)
        return JsonResponse({'result': 'OK',
                             'next': reverse('parse', args=(hs, ))})


class ParseView(View):

    def get(self, request, hex, *args, **kwargs):
        redis_name = 'parse_file_result_' + hex
        keys = r.hkeys(redis_name)
        result = r.hmget(redis_name, *keys)
        return JsonResponse(result)
