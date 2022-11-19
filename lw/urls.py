from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newsearch/', views.newsearch, name='newsearch'),
    path('instructionpage/', views.instructionpage, name='instructionpage'),
    path('register/', views.register, name='register'),
    path('update/<int:searchid>/', views.changesearchstate, name='searchstate'),
    path('delete/<int:searchid>/', views.removesearch, name='removesearch')
]