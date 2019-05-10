from django.urls import path, include, re_path

from ..views import views_wholeDNA


urlpatterns = [
    path('', views_wholeDNA.WholeDNAViews.wholeDNA_list),
    path('<int:pk>/', views_wholeDNA.WholeDNAViews.wholeDNA_detail, name='wholeDNA_detail'),
    re_path(r'^organism_id/(?P<organism_id>[\d]{1,15})$', views_wholeDNA.WholeDNAViews.wholeDNAByOrganism, name='organism_id'),
]
