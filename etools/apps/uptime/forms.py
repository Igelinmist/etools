from bootstrap3_datetime.widget import DateTimePicker

from django import forms
from datetime import timedelta

from .constants import INTERVAL_SET, EXT_INTERVAL_SET

class RecordForm(forms.Form):
    rdate = forms.DateField(
        widget=DateTimePicker(options={
            "startDate": "01.01.1945",
            "pickTime": False,
        }),
        label='Дата:',
    )
    wrk = forms.CharField()
    rsv = forms.CharField(required=False)
    arm = forms.CharField(required=False)
    trm = forms.CharField(required=False)
    krm = forms.CharField(required=False)
    srm = forms.CharField(required=False)
    rcd = forms.CharField(required=False)
    up_cnt = forms.IntegerField(initial=0, min_value=0)
    down_cnt = forms.IntegerField(initial=0, min_value=0)

    def __init__(self, *args, **kwargs):
        extended_stat = kwargs.pop('extended_stat', None)
        super(RecordForm, self).__init__(*args, **kwargs)
        for state_name in INTERVAL_SET:
            self.fields[state_name].initial = '0:00'
        # Если в журнале нет расширенной статистики удалить из формы лишние поля
        if not extended_stat:
            for state_name in EXT_INTERVAL_SET:
                self.fields.pop(state_name)