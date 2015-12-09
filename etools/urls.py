from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views

urlpatterns = patterns(
    'django.contrib.auth.views',
    url(r'^uptime/', include('uptime.urls', namespace="uptime")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^$', views.flatpage, {'url': '/home/'}, name='home'),
    url(r'^about/$', views.flatpage, {'url': '/about/'}, name='about'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
