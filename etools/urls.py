from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = patterns(
    'django.contrib.auth.views',
    url(r'^uptime/', include('uptime.urls', namespace="uptime")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'logout', name='logout'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
