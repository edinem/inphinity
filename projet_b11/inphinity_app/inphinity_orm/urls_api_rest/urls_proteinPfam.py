from django.urls import path, include

from ..views import views_proteinPfam


urlpatterns = [
    path('', views_proteinPfam.ProteinPFAMViews.proteinPfam_list),
    path('<int:pk>/', views_proteinPfam.ProteinPFAMViews.proteinPfam_detail),
]
