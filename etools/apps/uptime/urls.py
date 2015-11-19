from django.conf.urls import url

from .views import journal_views

urlpatterns = [
    url(r'^$', journal_views.index, name='index'),
    url(r'^(?P<journal_id>[0-9]+)/$', journal_views.show, name='show'),
    url(r'^(?P<journal_id>[0-9]+)/$', journal_views.show, name='show'),
    url(r'^(?P<journal_id>\d+)/record_new$', journal_views.record_new, name='record_new'),
    url(r'^(?P<journal_id>\d+)/record_edit/(?P<record_id>\d+)$', journal_views.record_edit, name='record_edit'),
    url(r'^(?P<journal_id>\d+)/record_delete/(?P<record_id>\d+)$',
        journal_views.record_delete,
        name='record_delete'),
    url(r'^records_on_date$', journal_views.records_on_date, name='records_on_date'),
    url(r'^silent_record_create_or_update$',
        journal_views.silent_record_create_or_update,
        name='silent_record_create_or_update'),
]
