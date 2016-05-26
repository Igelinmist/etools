from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from pcs.models.extern_data_models import Param
from pcs.models.report_models import Report
from pcs.forms import ChooseReportForm


def index(request):
    params = Param.objects.all()
    context = {'params': params}
    return render(request, 'pcs/index.html', context)


def reports(request):
    rtype = request.GET.get('rtype', 'hs')
    context = {'form': ChooseReportForm(None, rtype=rtype)}
    return render(request, 'pcs/reports.html', context)


def report_show(request):
    report_id = request.GET['report']
    if report_id:
        report = get_object_or_404(Report, pk=request.GET['report'])
        context = {
            'title': report.title,
            'tbl': report.prepare(request.GET['dt_from'], request.GET['dt_to'])
        }
        return render(request, 'pcs/report.html', context)
    else:
        return redirect('pcs:reports')


def report_form(request):
    pass


# JSON отклик со списком параметров для ограниченного ms_accronim
def find_params(request):
    if request.GET.get('param_set', None):
        param_set = request.GET.get('param_set')
        qs = {p.prmnum: p.__str__() for p in Param.objects.filter(ms_accronim=param_set).order_by('prmnum')}
    elif request.GET.get('rtype', None) == 'ahh':
        # 16777216 = 0x01000000 - флаг системы АИИС КУЭ
        qs = {p.prmnum: p.__str__() for p in Param.objects.extra(where=['enh_addr & 16777216 <> 0']).order_by('prmnum')}
    else:
        qs = {p.prmnum: p.__str__() for p in Param.objects.all()}
    return JsonResponse(qs)
