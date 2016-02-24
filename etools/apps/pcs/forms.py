from django import forms

from .models.extern_data_models import Param
from .models.report_models import Band


class BandForm(forms.ModelForm):
    param_choices = ((p.prmnum, p.__str__()) for p in Param.objects.all())
    param_num = forms.ChoiceField(choices=param_choices)

    class Meta:
        model = Band
        exclude = []
