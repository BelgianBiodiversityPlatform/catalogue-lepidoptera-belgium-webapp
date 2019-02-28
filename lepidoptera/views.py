from django.apps import apps
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.core.paginator import Paginator
import json

from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from lepidoptera.utils import get_source_version_info
from .models import Family, Subfamily, Species, Tribus, Genus, Subgenus, Province, TimePeriod, HostPlantSpecies, \
    HostPlantGenus, HostPlantFamily, HostPlantTaxonomicModel, Substrate, Observation, SpeciesPicture, Photographer, \
    ALL_LEPDIOPTERA_TAXON_MODELS


def home_page(request):
    valid_families = Family.objects.all()  # No support for synonyms at Family level => they're all valid.

    return render(request, 'lepidoptera/home.html', {'families': valid_families})


def all_species_for_taxon_json(request, model_name, id):
    Model = apps.get_model(app_label='lepidoptera', model_name=model_name)

    model_instance = get_object_or_404(Model, pk=id)
    return JsonResponse([s.json_for_species_lists for s in model_instance.all_species if s.is_valid], safe=False)


def family_page(request, family_id):
    family = get_object_or_404(Family, pk=family_id)

    return render(request, 'lepidoptera/taxonomy/family.html', {
        'taxon': family,
        'select_browse_menu': True
    })


def subfamily_page(request, subfamily_id):
    subfamily = get_object_or_404(Subfamily, pk=subfamily_id)

    return render(request, 'lepidoptera/taxonomy/subfamily.html', {
        'taxon': subfamily,
        'select_browse_menu': True})


def tribus_page(request, tribus_id):
    tribus = get_object_or_404(Tribus, pk=tribus_id)

    return render(request, 'lepidoptera/taxonomy/tribus.html', {
        'taxon': tribus,
        'select_browse_menu': True})


def genus_page(request, genus_id):
    genus = get_object_or_404(Genus, pk=genus_id)

    return render(request, 'lepidoptera/taxonomy/genus.html', {
        'taxon': genus,
        'select_browse_menu': True})


def subgenus_page(request, subgenus_id):
    subgenus = get_object_or_404(Subgenus, pk=subgenus_id)

    return render(request, 'lepidoptera/taxonomy/subgenus.html', {
        'taxon': subgenus,
        'select_browse_menu': True})


def species_page(request, species_id):
    species = get_object_or_404(Species, pk=species_id)

    context = {
        'taxon': species,
        'substrate_observations': Observation.objects.filter(species=species, substrate__isnull=False),
        'plant_species_observations': Observation.objects.filter(species=species, plant_species__isnull=False),
        'plant_genus_observations': Observation.objects.filter(species=species, plant_genus__isnull=False),
        'all_provinces': Province.objects.all(),
        'all_timeperiods': TimePeriod.objects.all(),

        'select_browse_menu': True
    }

    return render(request, 'lepidoptera/taxonomy/species.html', context)


def about_page(request):
    return render(request, 'lepidoptera/about.html', {
        'version_string': get_source_version_info()
    })


def browse_page(request):
    return render(request, 'lepidoptera/browse.html', {'select_browse_menu': True})


# All_xxx pages
def all_accepted_genera(request):
    genera = Genus.accepted_objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All accepted genera',
        'taxa': genera,
        'select_browse_menu': True
    })


def all_genera_synonyms(request):
    genera = Genus.synonym_objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All synonyms of genera',
        'taxa': genera,
        'select_browse_menu': True
    })


def all_accepted_species(request):
    species = Species.accepted_objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All accepted species',
        'taxa': species,
        'select_browse_menu': True
    })


def all_species_synonyms(request):
    species = Species.synonym_objects.all().order_by('name')

    return render(request, 'lepidoptera/taxonomy/all_xxx.html', {
        'title': 'All species synonym',
        'taxa': species,
        'select_browse_menu': True
    })


def hostplant_species(request, species_id):
    species = get_object_or_404(HostPlantSpecies, pk=species_id)

    return render(request, 'lepidoptera/hostplant_species.html', {
        'subject': species,
        'lepidoptera_species': species.lepidoptera_species.all,
        'select_browse_menu': True
    })


def hostplant_genus(request, genus_id):
    genus = get_object_or_404(HostPlantGenus, pk=genus_id)

    return render(request, 'lepidoptera/hostplant_genus.html', {
        'subject': genus,
        'lepidoptera_species': genus.lepidoptera_species.all,
        'select_browse_menu': True
    })


def hostplant_family(request, family_id):
    family = get_object_or_404(HostPlantFamily, pk=family_id)

    return render(request, 'lepidoptera/hostplant_family.html', {
        'subject': family,
        'select_browse_menu': True
    })


def substrate_page(request, substrate_id):
    substrate = get_object_or_404(Substrate, pk=substrate_id)

    return render(request, 'lepidoptera/substrate.html', {
        'subject': substrate,
        'lepidoptera_species': substrate.lepidoptera_species.all,
        'select_browse_menu': True
    })


def autocomplete(request, query_string):
    results = []

    models = HostPlantTaxonomicModel.__subclasses__()
    models.extend(ALL_LEPDIOPTERA_TAXON_MODELS)
    models.extend([Substrate])

    for model in models:
        instances = model.objects.filter(name__icontains=query_string)
        for instance in instances:
            results.append({
                'value': str(instance),
                'suggest_type': instance.suggest_type_label,
                'url': instance.get_absolute_url()
            })

    # Also look into Species vernacular names
    for vernacular_field_name in Species.VERNACULAR_FIELDS:
        lookup_string = '{}__icontains'.format(vernacular_field_name)
        args = {lookup_string: query_string}

        species = Species.objects.filter(**args)
        for s in species:
            results.append({
                'value': getattr(s, vernacular_field_name),
                'suggest_type': 'Vernacular name',
                'url': s.get_absolute_url()
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
        'HTMLMetadata': picture.html_metadata(full=True)
    } for picture in paginated_pictures]

    return JsonResponse({'hasMoreResults': paginated_pictures.has_next(),
                         'results': pictures_data,
                         'count': paginator.count}, safe=False)


def species_per_province_and_period(request):
    species_id = int(request.GET.get('speciesId'))

    sp = get_object_or_404(Species, pk=species_id)

    r = []

    # Time periods are always listed, even if no data
    for tp in TimePeriod.objects.all():
        r.append({
            'period_name': tp.name,
            'period_icon_url': tp.icon.url,
            'present_in': [presence.province.code for presence in sp.speciespresence_set.filter(present=True,
                                                                                                period=tp)]
        })

    return JsonResponse(r, safe=False)


def _sort_list_of_dicts_by_name(l):
    return sorted(l, key=lambda k: k['name'])


def _browse_model_json(model, title, name_attr='name', manager_name='objects'):
    try:
        model._meta.get_field(name_attr)
        name_attr_is_field = True
    except FieldDoesNotExist:
        name_attr_is_field = False

    manager = getattr(model, manager_name)
    qs = manager.all()

    if name_attr_is_field:  # in this case, we can order at the DB level
        qs = qs.order_by(name_attr)

    r = {
        'entries': [],
        'resultsTitle': title
    }

    for e in qs:
        entry = {'name': getattr(e, name_attr), 'link': e.get_absolute_url()}
        if hasattr(e, 'additional_data_for_json'):
            entry['additionalData'] = e.additional_data_for_json

        r['entries'].append(entry)

    if not name_attr_is_field:  # We have to sort in python
        r['entries'] = _sort_list_of_dicts_by_name(r['entries'])

    return JsonResponse(r, safe=False)


def browse_hostplants_families_json(request):
    return _browse_model_json(HostPlantFamily, 'Host plant families')


def browse_hostplants_genera_json(request):
    return _browse_model_json(HostPlantGenus, 'Host plant genera')


def browse_hostplants_species_json(request):
    return _browse_model_json(HostPlantSpecies, 'Host plant species', name_attr='html_str')


def browse_lepidoptera_families_json(request):
    return _browse_model_json(Family, 'Families')


def browse_lepidoptera_subfamilies_json(request):
    return _browse_model_json(Subfamily, 'Subfamilies')


def browse_lepidoptera_tribus_json(request):
    return _browse_model_json(Tribus, 'Tribus')


def browse_lepidoptera_genera_json(request):
    return _browse_model_json(Genus, 'Genera')


def browse_lepidoptera_subgenera_json(request):
    return _browse_model_json(Subgenus, 'Subgenera')


def browse_lepidoptera_species_json(request):
    return _browse_model_json(Species, 'Species', name_attr='binomial_name')


def browse_lepidoptera_non_native_species_json(request):
    return _browse_model_json(Species, 'Non-native species', name_attr='binomial_name', manager_name='non_native_objects')


def browse_substrates_json(request):
    return _browse_model_json(Substrate, 'Substates')


def browse_vernacularnames_json(request):
    qs = Species.objects.all()

    r = {
        'entries': [],
        'resultsTitle': 'Vernacular names'
    }

    for species in qs:
        for field_name in Species.VERNACULAR_FIELDS:
            val = getattr(species, field_name)
            if val is not None and val != '':
                r['entries'].append({'name': val, 'link': species.get_absolute_url()})

    r['entries'] = _sort_list_of_dicts_by_name(r['entries'])

    return JsonResponse(r, safe=False)


def haproxy_check(request):
    return HttpResponse('ok', content_type='text/plain')
