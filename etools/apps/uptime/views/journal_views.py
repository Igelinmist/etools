from django.shortcuts import render, get_object_or_404, redirect

from ..models.journal_models import Equipment, Journal
from ..forms import RecordForm


def index(request):
    root = Equipment.objects.filter(plant=None)[0]
    context = {'equipment_list': root.unit_tree()}
    return render(request, 'uptime/index.html', context)


def show(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    record_list = journal.get_last_records(depth=5)
    event_list = journal.events.order_by('-date')[:3]
    # TODO добавить форму для события
    context = {
        'journal': journal,
        'record_list': record_list,
        'event_list': event_list,
    }
    return render(request, 'uptime/show.html', context)


def record_new(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    form = RecordForm(request.POST or None, extended_stat=journal.downtime_stat)
    if request.POST and form.is_valid():
        journal.write_record(form.cleaned_data)
        if request.POST['submit'] == 'af':
            return redirect('uptime:show', journal_id=journal_id)
        else:
            rec, rdate = journal.switch_rec(request.POST['rdate'], request.POST['submit'])
            if rec:
                return redirect('uptime:record_edit', {'journal_id': journal_id, 'record_id': rec.id})
            else:
                form = RecordForm(
                    None,
                    extended_stat=journal.extended_stat,
                    initial={'rdate': rdate}
                )
                return render(
                    request,
                    'uptime/record_new.html',
                    {'form': form, 'journal': journal})
    return render(request, 'uptime/record_new.html', {'form': form, 'journal': journal})


def record_edit(request, journal_id, record_id):
    pass
