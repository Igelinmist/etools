from django.shortcuts import render

from .models.extern_data_models import Param


def index(request):
    params = Param.objects.all()
    context = {'params': params}
    return render(request, 'pcs/index.html', context)
