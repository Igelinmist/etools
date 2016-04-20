from django import forms

from bootstrap3_datetime.widgets import DateTimePicker

from ..constants import EVENT_CHOICES, STATE_SET, STATE_FNAME, STATE_SNAME


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


class RecordForm(forms.Form):
    """
    Universal record form. Base part has constant set of fields:
    1) Record date.
    2) UpCnt.
    3) DownCnt
    and undefined set of interval_in_state fields.
    """
    rdate = forms.CharField(widget=forms.TextInput(attrs={'size': 8, 'readonly': True}), label='Дата')
    up_cnt = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width:3.5em'}),
                                initial=0, min_value=0, label="Пуски")
    down_cnt = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width:3.5em'}),
                                  initial=0, min_value=0, label="Остановы")

    def __init__(self, *args, **kwargs):
        journal = kwargs.pop('journal')
        time_in_state = {state: kwargs.pop(state, None) for state in STATE_SET}
        is_individual = kwargs.pop('is_individual', False)

        super(RecordForm, self).__init__(*args, **kwargs)
        if is_individual:
            self.fields['rdate'] = forms.DateField(
                widget=DateTimePicker(options={"startDate": "01.01.1945", "pickTime": False, }),
                label='Дата:',
            )
            for st_name, st_flag in journal.control_flags:
                if st_flag:
                    self.fields[st_name] = forms.CharField(
                        widget=forms.TextInput(attrs={'size': 4, 'class': 'interval',
                                                      'pattern': '([0-9]{1,6}):[0-5][0-9]'}),
                        initial=time_in_state[st_name] if time_in_state[st_name] else '0:00',
                        label=STATE_FNAME[st_name])
        else:
            for st_name, st_flag in journal.control_flags:
                if st_flag:
                    self.fields[st_name] = forms.CharField(
                        widget=forms.TextInput(attrs={'size': 4, 'class': 'interval',
                                                      'pattern': '([0-9]{1,6}):[0-5][0-9]'}),
                        initial=time_in_state[st_name] if time_in_state[st_name] else '0:00',
                        label=STATE_SNAME[st_name])
