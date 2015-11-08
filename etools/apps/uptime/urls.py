from django.conf.urls import url

from .views import journal_views

urlpatterns = [
    url(r'^$', journal_views.index, name='index'),
    url(r'^(?P<journal_id>[0-9]+)/$', journal_views.show, name='show'),
    url(r'^(?P<journal_id>[0-9]+)/$', journal_views.show, name='show'),
    url(r'^(?P<journal_id>\d+)/record_new$', journal_views.record_new, name='record_new'),
    url(r'^(?P<journal_id>\d+)/record_edit/(?P<record_id>\d+)$', journal_views.record_edit, name='record_edit'),
]
