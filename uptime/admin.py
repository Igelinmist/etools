from django.contrib import admin

from uptime.models.journal_models import Equipment, Journal

admin.site.register(Equipment)
admin.site.register(Journal)
