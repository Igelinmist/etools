from django import forms


class BaseRecordForm(forms.Form):

    rdate = forms.CharField(widget=forms.TextInput(attrs={'size': 10}), label='Дата')
    wrk = forms.CharField(widget=forms.TextInput(attrs={'size': 5}), initial='0:00', label='Работа')
    up_cnt = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width:40px'}),
                                initial=0, min_value=0, label="Пуски")
    down_cnt = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width:40px'}),
                                  initial=0, min_value=0, label="Остановы")


class DownStatRecordForm(BaseRecordForm):
    rsv = forms.CharField(widget=forms.TextInput(attrs={'size': 5}), initial='0:00', label='Рез.')
    arm = forms.CharField(widget=forms.TextInput(attrs={'size': 5}), initial='0:00', label='АвРем')
    trm = forms.CharField(widget=forms.TextInput(attrs={'size': 5}), initial='0:00', label='ТекРем')
    krm = forms.CharField(widget=forms.TextInput(attrs={'size': 5}), initial='0:00', label='КапРем')
    srm = forms.CharField(widget=forms.TextInput(attrs={'size': 5}), initial='0:00', label='СрРем')
    rcd = forms.CharField(widget=forms.TextInput(attrs={'size': 5}), initial='0:00', label='Рек')


class HotReservRecordForm(BaseRecordForm):
    hrs = forms.CharField(widget=forms.TextInput(attrs={'size': 6}), initial='0:00')
