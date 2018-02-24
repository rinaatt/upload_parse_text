import logging
from django.views.generic import TemplateView, FormView
from .forms import UploadForm

log = logging.getLogger('app.text_parse')


class IndexView(FormView):
    form_class = UploadForm
    template_name = 'text_parse/index.html'
    success_url = '/text-parse/'

    def form_valid(self, form):
        file = form.cleaned_data['file']
        log.debug('Get file with length: %s', len(file.read()))
        return super().form_valid(form)
