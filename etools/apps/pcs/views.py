from django.shortcuts import render, redirect, get_object_or_404

from .models.extern_data_models import Param
from .models.report_models import Report
from .forms import ChooseReportForm


def index(request):
    params = Param.objects.all()
    context = {'params': params}
    return render(request, 'pcs/index.html', context)


def reports(request):
    context = {'form': ChooseReportForm(None)}
    return render(request, 'pcs/reports.html', context)


def report_show(request):
    report_id = request.GET['report']
    if report_id:
        report = get_object_or_404(Report, pk=request.GET['report'])
        context = {'report_id': report.id}
        return render(request, 'pcs/report.html', context)
    else:
        return redirect('pcs:reports')
