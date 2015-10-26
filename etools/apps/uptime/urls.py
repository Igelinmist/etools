from django.conf.urls import url

from uptime.views import journal_views

urlpatterns = [
    url(r'^$',
        journal_views.index,
        name='index'),
]
