from .models import Family, Subfamily


def stats_processor(request):
    return {'family_counter': Family.objects.count(),
            'subfamily_counter': Subfamily.objects.count()}
