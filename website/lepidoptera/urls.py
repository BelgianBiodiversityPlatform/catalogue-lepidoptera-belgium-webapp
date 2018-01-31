from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.home_page, name='home'),
    path('family/<int:family_id>/', views.family_page, name='family_page'),

]