import logging
from django.views.generic import TemplateView, View
from django.http.response import JsonResponse

log = logging.getLogger('app.text_parse')


class IndexView(TemplateView):
    template_name = 'text_parse/index.html'


class UploadView(View):

    def post(self, request, *args, **kwargs):
        file_data = request.POST['data']
        file_name = request.POST['name']
        log.debug('Get file with length: %s', len(file_data))
        return JsonResponse({'result': 'OK'})
