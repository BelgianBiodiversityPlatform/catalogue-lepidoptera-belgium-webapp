from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),

    path('family/<int:family_id>/', views.family_page, name='family_page'),
    path('subfamily/<int:subfamily_id>/', views.subfamily_page, name='subfamily_page'),
    path('tribus/<int:tribus_id>/', views.tribus_page, name='tribus_page'),
    path('genus/<int:genus_id>/', views.genus_page, name='genus_page'),
    path('subgenus/<int:subgenus_id>/', views.subgenus_page, name='subgenus_page'),
    path('species/<int:species_id>/', views.species_page, name='species_page'),

    path('families/', views.all_families, name='families_page'),

    path('hostplant/species/<int:species_id>/', views.hostplant_species, name='hostplant_species_page'),
    path('hostplant/genus/<int:genus_id>/', views.hostplant_genus, name='hostplant_genus_page'),
    path('hostplant/family/<int:family_id>/', views.hostplant_family, name='hostplant_family_page'),
    path('substrate/<int:substrate_id>/', views.substrate_page, name='substrate_page'),

    path('search_autocomplete/<str:query_string>', views.autocomplete, name='search_autocomplete')
]