#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include, re_path

from ..views import views_protein


urlpatterns = [
    path('', views_protein.ProteinViews.protein_list),
    path('<int:pk>/', views_protein.ProteinViews.protein_detail, name='protein_detail'),
    re_path(r'^organism_id/(?P<organism_id>[\d]{1,15})$', views_protein.ProteinViews.protein_by_organism, name='protein_organism_id'),
]

 