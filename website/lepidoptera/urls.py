from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='home'),

    path('family/<int:family_id>/', views.family_page, name='family_page'),
    path('subfamily/<int:subfamily_id>/', views.subfamily_page, name='subfamily_page'),
    path('tribus/<int:tribus_id>/', views.tribus_page, name='tribus_page'),
    path('genus/<int:genus_id>/', views.genus_page, name='genus_page'),
    path('subgenus/<int:subgenus_id>/', views.subgenus_page, name='subgenus_page'),
    path('species/<int:species_id>/', views.species_page, name='species_page')
]