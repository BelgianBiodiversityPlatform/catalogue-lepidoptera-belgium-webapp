from django.conf import settings
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.shortcuts import render

from .models import Family, Subfamily, Species, Tribus, Genus, Subgenus, Province, TimePeriod, TaxonomicModel, \
    HostPlantSpecies, HostPlantGenus, HostPlantFamily, HostPlantTaxonomicModel, Substrate, Observation, SpeciesPicture, \
    Photographer


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

    context = {
        'taxon': species,
        'substrate_observations': Observation.objects.filter(species=species, substrate__isnull=False),
        'plant_species_observations': Observation.objects.filter(species=species, plant_species__isnull=False),
        'plant_genus_observations': Observation.objects.filter(species=species, plant_genus__isnull=False),
        'species_as_a_list': [species],
        'all_provinces': Province.objects.all(),
        'all_timeperiods': TimePeriod.objects.all()
    }

    return render(request, 'lepidoptera/taxonomy/species.html', context)


def about_page(request):
    return render(request, 'lepidoptera/about.html')


def browse_page(request):
    return render(request, 'lepidoptera/browse.html')

# All_xxx pages

def all_families(request):
    families = Family.objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All families',
        'taxa': families
    })


def all_subfamilies(request):
    subfamilies = Subfamily.objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All subfamilies',
        'taxa': subfamilies
    })


def all_tribus(request):
    tribus = Tribus.objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All tribus',
        'taxa': tribus
    })


def all_accepted_genera(request):
    genera = Genus.accepted_objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All accepted genera',
        'taxa': genera
    })


def all_genera_synonyms(request):
    genera = Genus.synonym_objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All synonyms of genera',
        'taxa': genera
    })


def all_subgenera(request):
    subgenera = Subgenus.objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All subgenera',
        'taxa': subgenera
    })


def all_accepted_species(request):
    species = Species.accepted_objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All accepted species',
        'taxa': species
    })


def all_species_synonyms(request):
    species = Species.synonym_objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All species synonym',
        'taxa': species
    })


def all_hostplant_species(request):
    species = HostPlantSpecies.objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All host plant species',
        'taxa': species
    })


def all_hostplant_genera(request):
    genera = HostPlantGenus.objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All host plant genera',
        'taxa': genera
    })


def all_hostplant_families(request):
    families = HostPlantFamily.objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All host plant families',
        'taxa': families
    })


def all_substrates(request):
    substrates = Substrate.objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All substrates',
        'taxa': substrates
    })


def hostplant_species(request, species_id):
    species = HostPlantSpecies.objects.get(pk=species_id)

    return render(request, 'lepidoptera/hostplant_species.html', {
        'species': species,
        'lepidoptera_species': species.lepidoptera_species.all
    })


def hostplant_genus(request, genus_id):
    genus = HostPlantGenus.objects.get(pk=genus_id)

    return render(request, 'lepidoptera/hostplant_genus.html', {
        'genus': genus,
        'lepidoptera_species': genus.lepidoptera_species.all
    })


def hostplant_family(request, family_id):
    family = HostPlantFamily.objects.get(pk=family_id)

    return render(request, 'lepidoptera/hostplant_family.html', {
        'family': family
    })


def substrate_page(request, substrate_id):
    substrate = Substrate.objects.get(pk=substrate_id)

    return render(request, 'lepidoptera/substrate.html', {
        'substrate': substrate,
        'lepidoptera_species': substrate.lepidoptera_species.all
    })


# TODO: Implement more fields (vernacular names, ...) and models
def autocomplete(request, query_string):
    results = []
    models = HostPlantTaxonomicModel.__subclasses__()
    models.extend(TaxonomicModel.__subclasses__())
    models.extend([Substrate])

    for model in models:
        instances = model.objects.filter(name__icontains=query_string)
        for instance in instances:
            results.append({
                'value': str(instance),
                'suggest_type': instance.suggest_type_label,
                'url': instance.get_absolute_url()
            })

    return JsonResponse(results, safe=False)


def gallery_page(request):
    return render(request, 'lepidoptera/gallery.html', {
        'filters_choices': json.dumps({
            'specimenStages': SpeciesPicture.STAGES_CHOICES,
            'imageSubjects': SpeciesPicture.SUBJECT_CHOICES,
            'photographers': [
                {'id': photographer.pk, 'name': photographer.full_name} for photographer in Photographer.objects.all()
            ]
        })
    })


def pictures_json(request):
    page_number = request.GET.get('page')
    specimen_stage = request.GET.get('specimenStage')
    image_subject = request.GET.get('imageSubject')
    photographer_id = request.GET.get('photographer')

    pictures = SpeciesPicture.objects.all()

    if specimen_stage != '*':
        pictures = pictures.filter(specimen_stage=specimen_stage)

    if image_subject != '*':
        pictures = pictures.filter(image_subject=image_subject)

    if photographer_id != '*':
        if photographer_id == '':  # Pictures with no photographers set
            pictures = pictures.filter(photographer_id=None)
        else:
            pictures = pictures.filter(photographer_id=int(photographer_id))

    paginator = Paginator(pictures, settings.GALLERY_PAGE_SIZE)
    paginated_pictures = paginator.get_page(page_number)
    pictures_data = [{
        'thumbnaillURL': picture.image_thumbnail.url,
        'fullSizeURL': picture.image.url,
        'HTMLSpeciesName': picture.species.html_str_link(),
        'HTMLMetadata': picture.html_metadata()
    } for picture in paginated_pictures]

    return JsonResponse({'hasMoreResults': paginated_pictures.has_next(),
                         'results': pictures_data,
                         'count': paginator.count}, safe=False)


def species_per_province_and_period(request):
    species_id = int(request.GET.get('speciesId'))
    sp = Species.objects.get(pk=species_id)

    r = []

    # Time periods are always listed, even if no data
    for tp in TimePeriod.objects.all():
        r.append({
            'period_name': tp.name,
            'present_in': [presence.province.code for presence in sp.speciespresence_set.filter(present=True,
                                                                                                period=tp)]
        })

    return JsonResponse(r, safe=False)
