from django import forms
from django.urls import reverse


class UploadForm(forms.Form):
    file = forms.FileField(label='Файл')

    @property
    def action(self):
        return reverse('text_parse_index')
