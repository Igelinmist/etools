from django.contrib import admin

from .models.report_models import Report, Band
from .forms import BandForm


# class BandAdmin(admin.ModelAdmin):
#     form = BandForm

class BandInline(admin.TabularInline):
    model = Band
    form = BandForm
    extra = 1
    fieldsets = [(None, {'fields': ["param_set", "param_num", "name", "weight"]}), ]

    class Media:
        js = ("js/band_scripts.js",)


class ReportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'rtype', 'weight']}),
    ]
    inlines = [BandInline]

admin.site.register(Report, ReportAdmin)
# admin.site.register(Band, BandAdmin)
