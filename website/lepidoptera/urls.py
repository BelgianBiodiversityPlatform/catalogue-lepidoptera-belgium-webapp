from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='home'),

    path('family/<int:family_id>/', views.family_page, name='family_page'),
    path('subfamily/<int:subfamily_id>/', views.subfamily_page, name='subfamily_page'),
    path('species/<int:species_id>/', views.species_page, name='species_page')
]