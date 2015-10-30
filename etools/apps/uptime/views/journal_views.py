from django.shortcuts import render, get_object_or_404

from ..models.journal_models import Equipment, Journal


def index(request):
    root = Equipment.objects.filter(plant=None)[0]
    context = {'equipment_list': root.unit_tree()}
    return render(request, 'uptime/index.html', context)


def show(request, journal_id):
    journal = get_object_or_404(Journal, pk=journal_id)
    record_list = journal.get_last_records(depth=5)
    event_list = journal.events.order_by('-date')[:3]
    context = {
        'journal': journal,
        'record_list': record_list,
        'event_list': event_list,
    }
    return render(request, 'uptime/show.html', context)
