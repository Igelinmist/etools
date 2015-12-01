from django.shortcuts import get_object_or_404, render

from ..models.report_models import Report
from ..models.journal_models import Equipment
from ..forms.report_forms import ChooseReportForm


def reports(request):
    root = Equipment.objects.filter(plant=None)[0]
    if request.user.is_authenticated():
        try:
            root = request.user.profile.equipment
        except AttributeError:
            pass
    report_choices = Report.get_reports_collection(root)
    form = ChooseReportForm(choices=report_choices)

    return render(
        request,
        'uptime/reports.html',
        {'form': form, })


def report_show(request):
    report = get_object_or_404(Report, pk=request.GET['report_id'])
    context = {
        'rdata': report.prepare_reports_content(request.GET['date']),
        'rdate': request.GET['date'],
    }
    return render(
        request,
        'uptime/report.html',
        context
    )
