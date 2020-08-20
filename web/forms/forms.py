from django.forms import ModelForm

from .mixins import ReadonlyFormMixin


class ModelDisplayForm(ReadonlyFormMixin, ModelForm):
    pass
