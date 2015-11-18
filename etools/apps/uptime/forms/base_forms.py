from bootstrap3_datetime.widgets import DateTimePicker

from django import forms
# import floppyforms as forms

from ..constants import INTERVAL_SET, EXT_INTERVAL_SET


class RecordForm(forms.Form):
    rdate = forms.DateField(
        widget=DateTimePicker(options={"startDate": "01.01.1945", "pickTime": False, }),
        label='Дата:',
    )
    wrk = forms.CharField()
    rsv = forms.CharField()
    arm = forms.CharField()
    trm = forms.CharField()
    krm = forms.CharField()
    srm = forms.CharField()
    rcd = forms.CharField()
    up_cnt = forms.IntegerField(initial=0, min_value=0, label="Включений")
    down_cnt = forms.IntegerField(initial=0, min_value=0, label="Отключений")

    def __init__(self, *args, **kwargs):
        extended_stat = kwargs.pop('extended_stat', None)
        super(RecordForm, self).__init__(*args, **kwargs)
        for state_name in INTERVAL_SET:
            self.fields[state_name].initial = '0:00'
        # Если в журнале нет расширенной статистики удалить из формы лишние поля
        if not extended_stat:
            for state_name in EXT_INTERVAL_SET:
                self.fields.pop(state_name)
