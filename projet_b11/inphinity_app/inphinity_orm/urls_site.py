from django.urls import path, include
from . import views_site

#Tuto pour faire site web de consultation API

urlpatterns = [
    path('family/', views_site.family_all, name='family_all'),
    path('family/<int:fam_id>/', views_site.family_detail, name='family_detail'),
    path('family/new/', views_site.family_new, name='family_new'),
]
