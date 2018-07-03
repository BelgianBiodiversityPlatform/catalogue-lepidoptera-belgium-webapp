from django.urls import path

from . import views


def _get_browse_json_entry(name):
    return path(name, getattr(views, name), name=name)


urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),

    path('browse/', views.browse_page, name='browse'),
    _get_browse_json_entry('browse_hostplants_families_json'),
    _get_browse_json_entry('browse_hostplants_genera_json'),
    _get_browse_json_entry('browse_hostplants_species_json'),
    _get_browse_json_entry('browse_lepidoptera_families_json'),
    _get_browse_json_entry('browse_lepidoptera_subfamilies_json'),
    _get_browse_json_entry('browse_lepidoptera_tribus_json'),
    _get_browse_json_entry('browse_lepidoptera_genera_json'),
    _get_browse_json_entry('browse_lepidoptera_subgenera_json'),
    _get_browse_json_entry('browse_lepidoptera_species_json'),
    _get_browse_json_entry('browse_substrates_json'),
    _get_browse_json_entry('browse_vernacularnames_json'),

    path('gallery/', views.gallery_page, name='gallery'),
    path('pictures_json', views.pictures_json, name='pictures_json'),

    path('family/<int:family_id>/', views.family_page, name='family_page'),
    path('subfamily/<int:subfamily_id>/', views.subfamily_page, name='subfamily_page'),
    path('tribus/<int:tribus_id>/', views.tribus_page, name='tribus_page'),
    path('genus/<int:genus_id>/', views.genus_page, name='genus_page'),
    path('subgenus/<int:subgenus_id>/', views.subgenus_page, name='subgenus_page'),
    path('species/<int:species_id>/', views.species_page, name='species_page'),
    path('species_per_province_and_period/', views.species_per_province_and_period,
         name='species_per_province_and_period'),

    # All_xxx pages
    path('genera/accepted/', views.all_accepted_genera, name='all_accepted_genera_page'),
    path('genera/synonyms/', views.all_genera_synonyms, name='all_genera_synonyms_page'),
    path('species/accepted/', views.all_accepted_species, name='all_accepted_species_page'),
    path('species/synonyms/', views.all_species_synonyms, name='all_species_synonyms_page'),

    path('hostplant/species/<int:species_id>/', views.hostplant_species, name='hostplant_species_page'),
    path('hostplant/genus/<int:genus_id>/', views.hostplant_genus, name='hostplant_genus_page'),
    path('hostplant/family/<int:family_id>/', views.hostplant_family, name='hostplant_family_page'),
    path('substrate/<int:substrate_id>/', views.substrate_page, name='substrate_page'),

    path('search_autocomplete/<str:query_string>', views.autocomplete, name='search_autocomplete')
]