from django.views.generic import TemplateView, FormView
from .forms import UploadForm


class IndexView(FormView):
    form_class = UploadForm
    template_name = 'text_parse/index.html'
