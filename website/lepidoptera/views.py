from django.shortcuts import render

from .models import Family, Subfamily, Species, Tribus, Genus, Subgenus, Province, TimePeriod


def home_page(request):
    families = Family.valid_families_objects.all().order_by('display_order')

    return render(request, 'lepidoptera/home.html', {'families': families})


# TODO: factorize code for the taxonrank_page views?

def family_page(request, family_id):
    family = Family.objects.get(pk=family_id)

    return render(request, 'lepidoptera/taxonomy/family.html', {
        'family': family,
        'all_provinces': Province.objects.all(),
        'all_timeperiods': TimePeriod.objects.all()
    })


def subfamily_page(request, subfamily_id):
    subfamily = Subfamily.objects.get(pk=subfamily_id)

    return render(request, 'lepidoptera/taxonomy/subfamily.html', {'subfamily': subfamily})


def tribus_page(request, tribus_id):
    tribus = Tribus.objects.get(pk=tribus_id)

    return render(request, 'lepidoptera/taxonomy/tribus.html', {'tribus': tribus})


def genus_page(request, genus_id):
    genus = Genus.objects.get(pk=genus_id)

    return render(request, 'lepidoptera/taxonomy/genus.html', {'genus': genus})


def subgenus_page(request, subgenus_id):
    subgenus = Subgenus.objects.get(pk=subgenus_id)

    return render(request, 'lepidoptera/taxonomy/subgenus.html', {'subgenus': subgenus})


def species_page(request, species_id):
    species = Species.objects.get(pk=species_id)

    return render(request, 'lepidoptera/taxonomy/species.html', {'species': species})
