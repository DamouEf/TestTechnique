from django.urls import path

from . import views

urlpatterns = [
    path('runpagespeed/', views.RunpagespeedViews, name='runpagespeed'),
]