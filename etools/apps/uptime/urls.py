from django.conf.urls import url

from .views import journal_views

urlpatterns = [
    url(r'^$',
        journal_views.index,
        name='index'),
    url(r'^(?P<journal_id>[0-9]+)/$',
        journal_views.show,
        name='show'),
]
