from django.conf.urls import url

from .views import index
from .views import reports
from .views import report_show

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^reports$', reports, name='reports'),
    url(r'^reports/viewreport$',
        report_show,
        name='report_show'),
]
