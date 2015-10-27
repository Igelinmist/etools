from django.shortcuts import render, get_object_or_404

from ..models.journal_models import Equipment, Journal


def index(request):
    root = Equipment.objects.filter(plant=None)[0]
    context = {'equipment_list': root.unit_tree()}
    return render(request, 'uptime/index.html', context)


def show(request, journal_id):
    journal = get_object_or_404(Journal, journal_id)
    return render(request, 'uptime/show.html')
