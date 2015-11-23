from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models.journal_models import Equipment, Journal
from .models.employee_models import Employee
from .models.report_models import Report, Column


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name = 'сотрудник'
    verbose_name_plural = 'сотрудники'


class UserAdmin(UserAdmin):
    inlines = (EmployeeInline, )


class ColumnInline(admin.TabularInline):
    model = Column
    extra = 1


class ReportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'equipment', 'is_generalizing']}),
    ]
    inlines = [ColumnInline]

admin.site.register(Equipment)
admin.site.register(Journal)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Report, ReportAdmin)
