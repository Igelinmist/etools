from django.shortcuts import get_object_or_404, render, HttpResponse
from datetime import date

from ..models.report_models import Report
from ..models.journal_models import Equipment
from ..forms.report_forms import ChooseReportForm
from ..excel_utils import WriterToExcel


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
        'date': request.GET['date'],
        'date_from': request.GET['date_from'],
        'report_id': request.GET['report_id'],
    }
    if 'excel' in request.GET:
        response = HttpResponse(content_type='application/vnd.ms-excel')
        dtfrom = request.GET['date_from'] if request.GET['date_from'] else '01.01.1954'
        dtto = request.GET['date'] if request.GET['date'] else date.today().strftime("%d.%m.%Y")
        response['Content-Disposition'] = 'attachment; filename=rep_{}_{}.xlsx'.format(
            dtfrom, dtto)
        xlsx_data = WriterToExcel(context)
        response.write(xlsx_data)
        return response
    else:
        return render(
            request,
            'uptime/report.html',
            context
        )
