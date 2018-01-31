from django.shortcuts import render

from .models import Family


def home(request):
    families = Family.valid_families_objects.all().order_by('display_order')

    return render(request, 'lepidoptera/home.html', {'families': families})
