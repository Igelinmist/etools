from django import forms

from bootstrap3_datetime.widgets import DateTimePicker

from ..constants import EVENT_CHOICES


class BaseRecordForm(forms.Form):

    form_type = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'base'}), required=False)
    rdate = forms.CharField(widget=forms.TextInput(attrs={'size': 8, 'readonly': True}), label='Дата')
    wrk = forms.CharField(widget=forms.TextInput(attrs={'size': 4, 'class': 'interval'}), initial='0:00', label='Работа')
    up_cnt = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width:40px'}),
                                initial=0, min_value=0, label="Пуски")
    down_cnt = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width:40px'}),
                                  initial=0, min_value=0, label="Остановы")


class DownStatRecordForm(BaseRecordForm):
    form_type = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'down_stat'}), required=False)
    rsv = forms.CharField(widget=forms.TextInput(attrs={'size': 4, 'class': 'interval'}), initial='0:00', label='РЗ')
    arm = forms.CharField(widget=forms.TextInput(attrs={'size': 4, 'class': 'interval'}), initial='0:00', label='АР')
    trm = forms.CharField(widget=forms.TextInput(attrs={'size': 4, 'class': 'interval'}), initial='0:00', label='ТР')
    krm = forms.CharField(widget=forms.TextInput(attrs={'size': 4, 'class': 'interval'}), initial='0:00', label='КР')
    srm = forms.CharField(widget=forms.TextInput(attrs={'size': 4, 'class': 'interval'}), initial='0:00', label='СР')
    rcd = forms.CharField(widget=forms.TextInput(attrs={'size': 4, 'class': 'interval'}), initial='0:00', label='РК')


class HotReservRecordForm(BaseRecordForm):
    hrs = forms.CharField(widget=forms.TextInput(attrs={'size': 4, 'class': 'interval'}), initial='0:00')


class ChooseRecordsDateForm(forms.Form):
    rdate = forms.DateField(
        widget=DateTimePicker(options={"locale": "ru",
                                       "pickTime": False}),
        label='На дату:',
    )


class EventForm(forms.Form):
    date = forms.DateField(
        widget=DateTimePicker(options={"locale": "ru",
                                       "startDate": "01.01.1945",
                                       "pickTime": False}),
        label='Дата события:',
    )
    event_code = forms.ChoiceField(
        choices=EVENT_CHOICES,
        label='Событие',
    )
