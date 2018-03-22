from .models import Family, Subfamily, Tribus, Genus, Subgenus, Species, HostPlantSpecies, HostPlantFamily, \
    HostPlantGenus, Substrate


def stats_processor(request):
    return {
        'family_counter': Family.objects.count(),
        'subfamily_counter': Subfamily.objects.count(),
        'tribus_counter': Tribus.objects.count(),
        'valid_genus_counter': Genus.accepted_objects.count(),
        'genus_synonym_counter': Genus.synonym_objects.count(),
        'subgenus_counter': Subgenus.objects.count(),

        'valid_species_counter': Species.accepted_objects.count(),
        'species_synonym_counter': Species.synonym_objects.count(),

        'hostplant_species_counter': HostPlantSpecies.objects.count(),
        'hostplant_genus_counter': HostPlantGenus.objects.count(),
        'hostplant_family_counter': HostPlantFamily.objects.count(),
        'substrate_counter': Substrate.objects.count(),
    }
