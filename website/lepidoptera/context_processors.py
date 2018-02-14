from .models import Family, Subfamily, Tribus, Genus, Subgenus


def stats_processor(request):
    return {'family_counter': Family.objects.count(),
            'subfamily_counter': Subfamily.objects.count(),
            'tribus_counter': Tribus.objects.count(),
            'valid_genus_counter': Genus.accepted_objects.count(),
            'genus_synonym_counter': Genus.synonym_objects.count(),
            'subgenus_counter': Subgenus.objects.count()}
