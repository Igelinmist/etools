from django.shortcuts import render

from .models import Params


def index(request):
    params = Params.objects.all()
    context = {'params': params}
    return render(request, 'pcs/index.html', context)
