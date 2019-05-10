from django.urls import path, include, re_path

from ..views import views_contig


urlpatterns = [
    path('', views_contig.ContigViews.contig_list),
    path('<int:pk>/',  views_contig.ContigViews.contig_detail, name='contig_detail'),
    re_path(r'^organism_id/(?P<organism_id>[\d]{1,15})$', views_contig.ContigViews.contigsByOrganism, name='organism_id'),
]
