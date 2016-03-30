from django.shortcuts import get_object_or_404, render

from ..models.report_models import Report
from ..models.journal_models import Equipment
from ..forms.report_forms import ChooseReportForm


def reports(request):
    try:
        head_unit = request.user.profile.equipment
    except AttributeError:
        head_unit = Equipment.objects.filter(plant=None)[0]
    head_unit = Equipment.objects.filter(plant=None)[0]
    if request.user.is_authenticated():
        try:
            head_unit = request.user.profile.equipment
        except AttributeError:
            pass
    report_choices = Report.get_reports_collection(head_unit)
    form = ChooseReportForm(choices=report_choices)

    return render(
        request,
        'uptime/reports.html',
        {'form': form, })


def report_show(request):
    report = get_object_or_404(Report, pk=request.GET['report_id'])
    context = {
        'rdata': report.prepare_reports_content(request.GET['date'], request.GET['date_from']),
        'rdate': request.GET['date'],
        'rdate_from': request.GET['date_from'],
    }
    return render(
        request,
        'uptime/report.html',
        context
    )
