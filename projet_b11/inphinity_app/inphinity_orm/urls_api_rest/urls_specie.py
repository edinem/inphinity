from django.urls import path, include

from ..views import views_specie


urlpatterns = [
    path('', views_specie.SpecieViews.specie_list),
    path('<int:pk>/', views_specie.SpecieViews.specie_detail, name='specie_detail'),
]
