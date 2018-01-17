from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.home, name='home'),

]