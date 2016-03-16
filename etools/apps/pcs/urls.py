from django.conf.urls import url

from .views import index
from .views import reports
from .views import report_show
from .views import report_form
from .views import find_params

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^reports/$', reports, name='reports'),
    url(r'^reports/viewreport$',
        report_show,
        name='report_show'),
    url(r'^reports/form$', report_form, name='report_form'),
    url(r'^find_params/$', find_params, name='find_params'),
]
