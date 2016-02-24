from django.db import models


REPORT_TYPES = (
    ('hs', 'Часовые срезы'),
    ('ahh', 'Средняя мощность за 30 мин'),
)


class Report(models.Model):
    """
    Description: Class Report - representation of technological data
    """
    title = models.CharField(max_length=100)
    weight = models.IntegerField(default=0)
    rtype = models.CharField(max_length=3, choices=REPORT_TYPES)

    class Meta:
        verbose_name = 'отчет'
        verbose_name_plural = 'отчеты'
        ordering = ['weight']

    def __str__(self):
        return self.title


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
    name = models.CharField(max_length=15)
    weight = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'лента'
        verbose_name_plural = 'ленты'
        ordering = ['weight']
        default_permissions = []

    def __str__(self):
        return "[%s] %s" % (self.param_num, self.name)
