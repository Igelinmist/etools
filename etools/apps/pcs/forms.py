from django import forms

from bootstrap3_datetime.widgets import DateTimePicker

from pcs.models.extern_data_models import Param
from pcs.models.report_models import Report
from pcs.models.report_models import Band

param_choices = [(None, '----'), ] + [(p.prmnum, p.__str__()) for p in Param.objects.all().order_by('prmnum')]


class BandForm(forms.ModelForm):
    param_set = forms.ChoiceField(
        label='Набор параметров',
        choices=(
            (None, '---'),
            ('OF', 'Общесистемные'),
            ('T3', 'ТЭЦ-3 - общестанционные'),
            ('T3EL', 'ТЭЦ-3 - электроустановка'),
            ('T3GAZ', 'ТЭЦ-3 - топливо'),
            ('T4', 'ТЭЦ-4 - общестанционные'),
            ('T4EL', 'ТЭЦ-4 - электроустановка'),
            ('T4TOPLIVO', 'ТЭЦ-4 - топливо'),
            ('T5', 'ТЭЦ-5 - общестанционные'),
            ('T5EL', 'ТЭЦ-5 - электроустановка'),
            ('T5TS', 'ТЭЦ-5 - теплосеть'),
            ('KRK', 'КРК - общестанционные'),
            ('KRKTOPLIVO', 'КРК - топливо'),
            ('KRKTS', 'КРК - теплосеть'),
            ('T2', 'ТЭЦ-2 - общестанционные'),
            ('T2GAZ', 'ТЭЦ-2 - топливо'),
            ),
        widget=forms.Select(attrs={
            "class": 'prmsets', }),
        required=False,
    )
    param_num = forms.ChoiceField(
        label='Параметр',
        choices=param_choices,
        widget=forms.Select(
            attrs={"class": 'prmchoice', }
        )
    )

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

    def __init__(self, *args, **kwargs):
        rtype = kwargs.pop('rtype', None)
        super(ChooseReportForm, self).__init__(*args, **kwargs)
        if rtype:
            self.fields['report'].queryset = Report.objects.filter(rtype=rtype)
