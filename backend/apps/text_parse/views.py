import logging
from django.views.generic import TemplateView, View
from django.http.response import JsonResponse


log = logging.getLogger('app.text_parse')


class IndexView(TemplateView):
    template_name = 'text_parse/index.html'


class UploadView(View):

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        log.debug('Got file: %r with size: %d', file, file.size)
        return JsonResponse({'result': 'OK', 'fileSize': file.size})
