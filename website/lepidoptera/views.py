from django.shortcuts import render

from .models import Family


def home_page(request):
    families = Family.valid_families_objects.all().order_by('display_order')

    return render(request, 'lepidoptera/home.html', {'families': families})


def family_page(request, family_id):
    family = Family.objects.get(pk=family_id)

    return render(request, 'lepidoptera/family.html', {'family': family})
