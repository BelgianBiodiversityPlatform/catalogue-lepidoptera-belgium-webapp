from .models import Family, Subfamily, Tribus


def stats_processor(request):
    return {'family_counter': Family.objects.count(),
            'subfamily_counter': Subfamily.objects.count(),
            'tribus_counter': Tribus.objects.count()}
