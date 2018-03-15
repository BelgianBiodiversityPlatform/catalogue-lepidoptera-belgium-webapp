from django.http import JsonResponse
from django.shortcuts import render

from .models import Family, Subfamily, Species, Tribus, Genus, Subgenus, Province, TimePeriod, TaxonomicModel, \
    HostPlantSpecies


def home_page(request):
    valid_families = Family.valid_families_objects.all().order_by('display_order')

    return render(request, 'lepidoptera/home.html', {'families': valid_families})


# TODO: factorize code for the taxonrank_page views?

def family_page(request, family_id):
    family = Family.objects.get(pk=family_id)

    return render(request, 'lepidoptera/taxonomy/family.html', {
        'taxon': family,
        'all_provinces': Province.objects.all(),
        'all_timeperiods': TimePeriod.objects.all()
    })


def subfamily_page(request, subfamily_id):
    subfamily = Subfamily.objects.get(pk=subfamily_id)

    return render(request, 'lepidoptera/taxonomy/subfamily.html', {'taxon': subfamily})


def tribus_page(request, tribus_id):
    tribus = Tribus.objects.get(pk=tribus_id)

    return render(request, 'lepidoptera/taxonomy/tribus.html', {'taxon': tribus})


def genus_page(request, genus_id):
    genus = Genus.objects.get(pk=genus_id)

    return render(request, 'lepidoptera/taxonomy/genus.html', {'taxon': genus})


def subgenus_page(request, subgenus_id):
    subgenus = Subgenus.objects.get(pk=subgenus_id)

    return render(request, 'lepidoptera/taxonomy/subgenus.html', {'taxon': subgenus})


def species_page(request, species_id):
    species = Species.objects.get(pk=species_id)

    return render(request, 'lepidoptera/taxonomy/species.html', {'taxon': species})


def about_page(request):
    return render(request, 'lepidoptera/about.html')


def all_families(request):
    families = Family.objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/families.html', {'families': families})


def hostplant_species(request, species_id):
    species = HostPlantSpecies.objects.get(pk=species_id)

    return render(request, 'lepidoptera/hostplant_species.html', {'species': species})


# TODO: Implement more fields (vernacular names, ...) and models
def autocomplete(request, query_string):
    results = []
    models = [HostPlantSpecies]
    models.extend(TaxonomicModel.__subclasses__())

    for model in models:
        instances = model.objects.filter(name__icontains=query_string)
        for instance in instances:
            results.append({
                'value': str(instance),
                'suggest_type': instance._meta.model_name,
                'url': instance.get_absolute_url()
            })

    return JsonResponse(results, safe=False)