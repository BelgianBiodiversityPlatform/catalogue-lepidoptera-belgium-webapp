from .models import Family, Subfamily, Tribus


def stats_processor(request):
    return {'family_counter': Family.objects.count(),
            'subfamily_counter': Subfamily.objects.count(),
            'tribus_counter': Tribus.objects.count(),
            'valid_genus_counter': 5,
            'genus_synonym_counter': 2}
