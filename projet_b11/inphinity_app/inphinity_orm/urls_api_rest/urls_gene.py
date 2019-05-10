from django.urls import path, include

from ..views import views_gene


urlpatterns = [
    path('', views_gene.GeneViews.gene_list),
    path('<int:pk>/', views_gene.GeneViews.gene_detail, name='gene_detail'),
]
