from django.contrib import admin

from .models.report_models import Report, Band

admin.site.register(Report)
admin.site.register(Band)
