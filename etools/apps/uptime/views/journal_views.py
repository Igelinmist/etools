from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

from ..models.journal_models import Equipment, Journal, EventItem
from ..forms.journal_forms import EventForm, RecordForm, ChooseRecordsDateForm
from ..utils import yesterday_local, custom_redirect


def index(request):
    head_unit = Equipment.objects.filter(plant=None)[0]
    if request.user.is_authenticated():
        try:
            head_unit = request.user.profile.equipment
        except AttributeError:
            pass
    context = {'equipment_list': head_unit.unit_tree()}
    return render(request, 'uptime/index.html', context)


def show(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    record_list = journal.get_last_records(depth=5)
    event_list = journal.events.order_by('-date')[:3]
    form = EventForm(None)
    context = {
        'journal': journal,
        'record_list': record_list,
        'event_list': event_list,
        'form': form,
    }
    return render(request, 'uptime/show.html', context)


def journal_description_update(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    journal.description = request.POST['description']
    journal.save(update_fields=['description'])
    messages.add_message(request, messages.SUCCESS, 'Описание успешно обновлено!')
    return JsonResponse({'status': 0})


@permission_required('uptime.create_journal_record', login_url='login')
def record_new(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    rdate = request.GET.get('rdate', yesterday_local())
    form = RecordForm(request.POST or None, journal=journal, is_individual=True, initial={'rdate': rdate})
    if request.POST and form.is_valid():
        journal.write_record(**form.cleaned_data)
        if request.POST['submit'] == 'af':
            return redirect('uptime:show', journal_id=journal_id)
        else:
            rec, rdate = journal.switch_date_get_rec(request.POST['rdate'], request.POST['submit'])
            if rec:
                return redirect('uptime:record_edit', journal_id=journal.id, record_id=rec.id)
            else:
                return custom_redirect('uptime:record_new', journal.id, rdate=rdate)
    return render(request, 'uptime/record_new.html', {'form': form, 'journal': journal})


@permission_required('uptime.edit_journal_record', login_url='login')
def record_edit(request, journal_id, record_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = RecordForm(request.POST or journal.get_record_data(record_id), journal=journal, is_individual=True)
    if request.POST and form.is_valid():
        journal.write_record(**form.cleaned_data)
        if request.POST['submit'] == 'af':
            return redirect('uptime:show', journal_id=journal_id)
        else:
            rec, rdate = journal.switch_date_get_rec(request.POST['rdate'], request.POST['submit'])
            if rec:
                return redirect('uptime:record_edit', journal_id=journal.id, record_id=rec.id)
            else:
                return custom_redirect('uptime:record_new', journal.id, rdate=rdate)
    return render(request, 'uptime/record_edit.html', {'form': form, 'journal': journal, 'record_id': record_id})


@permission_required('uptime.delete_journal_record', login_url='login')
def record_delete(request, journal_id, record_id):
    template_name = 'uptime/confirm_record_delete.html'
    journal = get_object_or_404(Journal, pk=journal_id)
    if request.method == 'POST':
        journal.delete_record(record_id)
        return redirect('uptime:show', journal_id=journal_id)
    return render(request, template_name)


@permission_required('uptime.create_journal_record', login_url='login')
def records_on_date(request):
    template_name = 'uptime/records_on_date.html'
    rdate = request.POST.get('rdate', yesterday_local())
    form_date = ChooseRecordsDateForm(initial={'rdate': rdate})
    try:
        head_unit = request.user.profile.equipment
    except AttributeError:
        head_unit = Equipment.objects.filter(plant=None)[0]
    data_table = head_unit.collect_sub_stat_on_date(rdate)
    for row in data_table:
        if 'journal_id' in row:
            row['form_content'] = RecordForm(row['rec_data'],
                                             journal=Journal.objects.get(pk=row['journal_id']),
                                             auto_id=False)
    context = {'rdate': rdate, 'data_table': data_table, 'form_date': form_date}
    return render(request, template_name, context)


@permission_required('uptime.create_journal_record', login_url='login')
def silent_record_create_or_update(request):
    journal = get_object_or_404(Journal, pk=request.POST['journal_id'])
    if request.is_ajax():
        form = RecordForm(request.POST, journal=journal)
        if form.is_valid():
            journal.write_record(**form.cleaned_data)
            response = {'status': 0, 'journal_id': request.POST['journal_id']}
    else:
        response = {'status': -1}
    return JsonResponse(response)


def records(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    all_records = journal.records.order_by('-rdate').all()
    paginator = Paginator(all_records, 25)
    page = request.GET.get('page')
    try:
        paged_records = paginator.page(page)
    except PageNotAnInteger:
        paged_records = paginator.page(1)
    except EmptyPage:
        paged_records = paginator.page(paginator.num_pages)
    return render(
        request,
        'uptime/records.html',
        {'record_list': paged_records, 'journal': journal})


@permission_required('uptime.create_journal_event', login_url='login')
def event_create(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = EventForm(request.POST)
    if request.POST and form.is_valid():
        journal.set_event_data(form.cleaned_data)
    return redirect('uptime:show', journal_id=journal_id)


@permission_required('uptime.delete_journal_event', login_url='login')
def event_delete(request, journal_id, event_id):
    template_name = 'uptime/confirm_record_delete.html'
    event = get_object_or_404(EventItem, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('uptime:show', journal_id=journal_id)
    return render(request, template_name)
