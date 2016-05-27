from django.db import models
from datetime import datetime, timedelta

from pcs.models.extern_data_models import Param
from pcs.utils import round_tm_30_up


REPORT_TYPES = (
    ('hs', 'Часовые срезы'),
    ('ahh', 'Средняя мощность за 30 мин'),
)


class Report(models.Model):
    """
    Description: Class Report - representation of technological data
    """
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    weight = models.IntegerField(default=0, verbose_name='Вес')
    rtype = models.CharField(max_length=3, choices=REPORT_TYPES, verbose_name='Тип отчета')

    class Meta:
        verbose_name = 'отчет'
        verbose_name_plural = 'отчеты'
        ordering = ['weight']

    def __str__(self):
        return self.title

    def prepare(self, dtfrom_str, dtto_str):
        """
        Prepare content of Report
        """
        # Calculate time_row
        dtfrom = datetime.strptime(dtfrom_str, "%d.%m.%Y %H:%M")
        dtto = datetime.strptime(dtto_str, "%d.%m.%Y %H:%M")
        res = {
            'rtitles': [],
            'content': [],
        }
        if dtfrom > dtto:
            return res
        if self.rtype == 'hs':
            #  Округление до часа
            dttemp = datetime(dtfrom.year, dtfrom.month, dtfrom.day, dtfrom.hour)
            if dttemp == dtfrom:
                res['rtitles'].append(dttemp)
            #  Заполнение заголовков
            while dttemp <= dtto:
                dttemp += timedelta(hours=1)
                if dttemp <= dtto:
                    res['rtitles'].append(dttemp)
            for band in self.bands.all():
                prm = Param.objects.get(pk=band.param_num)
                hist_data = prm.get_slice_data(dtfrom, dtto)
                hrow = []
                for tm in res['rtitles']:
                    tv = hist_data['ctrl_tm'].get(tm, '-')
                    if tv != '-':
                        tv = tv.v
                    hrow.append(tv)
                res['content'].append([band.name, ] + hrow)
        elif self.rtype == 'ahh':
            dttemp = round_tm_30_up(dtfrom)
            #  Заполнение заголовков
            res['rtitles'].append(dttemp)
            while dttemp <= dtto:
                dttemp += timedelta(minutes=30)
                res['rtitles'].append(dttemp)
            for band in self.bands.all():
                prm = Param.objects.get(pk=band.param_num)
                # Интервал берем заведомо больший, чтобы учесть ведущие и завершающие дельты
                hist_data = prm.get_30p_data(dtfrom - timedelta(minutes=30), dtto + timedelta(minutes=30))
                hrow = []
                for tm in res['rtitles']:
                    tv = hist_data['ctrl_tm'].get(tm, '-')
                    hrow.append(tv)
                res['content'].append([band.name, ] + hrow)
        return res


class Band(models.Model):
    """
    Description: Class Band is a line Report
    """
    report = models.ForeignKey(
        Report,
        related_name='bands',
        on_delete=models.CASCADE
    )
    param_num = models.IntegerField()
    name = models.CharField(max_length=50, verbose_name='Имя для отчета')
    weight = models.IntegerField(default=0, verbose_name='Вес')

    class Meta:
        verbose_name = 'лента'
        verbose_name_plural = 'ленты'
        ordering = ['weight']
        default_permissions = []

    def __str__(self):
        return "[%s] %s" % (self.param_num, self.name)
