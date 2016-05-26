from django.contrib import admin

from pcs.models.report_models import Report, Band
from pcs.models.extern_data_models import Param
from pcs.forms import BandForm


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

admin.site.register(Param)
admin.site.register(Report, ReportAdmin)
# admin.site.register(Band, BandAdmin)
