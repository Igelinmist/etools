from django.contrib import admin

from .models.report_models import Report, Band
from .forms import BandForm


class BandAdmin(admin.ModelAdmin):
    form = BandForm

admin.site.register(Report)
admin.site.register(Band, BandAdmin)
