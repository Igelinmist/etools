from django import forms

from bootstrap3_datetime.widgets import DateTimePicker

from .models.extern_data_models import Param
from .models.report_models import Report
from .models.report_models import Band

param_choices = ((p.prmnum, p.__str__()) for p in Param.objects.all())


class BandForm(forms.ModelForm):
    param_num = forms.ChoiceField(choices=param_choices)

    class Meta:
        model = Band
        exclude = []


class ChooseReportForm(forms.Form):
    report = forms.ModelChoiceField(
        widget=forms.widgets.RadioSelect(),
        queryset=Report.objects.all(),
        empty_label='',
        label='Отчет',
    )
    dt_from = forms.DateTimeField(
        widget=DateTimePicker(options={"locale": "ru",
                                       "pickTime": True}),
        label='Начало отчета:',
    )
    dt_to = forms.DateTimeField(
        widget=DateTimePicker(options={"locale": "ru",
                                       "pickTime": True}),
        label='Конец отчета:',
    )
