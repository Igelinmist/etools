from django import forms

from bootstrap3_datetime.widgets import DateTimePicker


class ChooseReportForm(forms.Form):
    date_from = forms.DateField(
        widget=DateTimePicker(options={"locale": "ru",
                                       "pickTime": False,
                                       "startDate": "1/1/1953"}),
        label='От даты:',
    )

    date = forms.DateField(
        widget=DateTimePicker(options={"locale": "ru",
                                       "pickTime": False,
                                       "startDate": "1/1/1953"}),
        label=', на дату:',
    )

    def __init__(self, choices=None, *args, **kwargs):
        super(ChooseReportForm, self).__init__(*args, **kwargs)
        if choices:
            self.fields.update(
                {'report_id': forms.ChoiceField(widget=forms.Select,
                                                label='отчет:',
                                                choices=choices)}
            )
