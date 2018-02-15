from django.shortcuts import render

from .models import Family, Subfamily, Species


def home_page(request):
    families = Family.valid_families_objects.all().order_by('display_order')

    return render(request, 'lepidoptera/home.html', {'families': families})


def family_page(request, family_id):
    family = Family.objects.get(pk=family_id)

    return render(request, 'lepidoptera/taxonomy/family.html', {'family': family})


def subfamily_page(request, subfamily_id):
    subfamily = Subfamily.objects.get(pk=subfamily_id)

    return render(request, 'lepidoptera/taxonomy/subfamily.html', {'subfamily': subfamily})


def species_page(request, species_id):
    species = Species.objects.get(pk=species_id)

    return render(request, 'lepidoptera/taxonomy/species.html', {'species': species})
