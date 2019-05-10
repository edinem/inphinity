from django.urls import path, include

from ..views import views_genus


urlpatterns = [
    path('', views_genus.GenusViews.genus_list),
    path('<int:pk>/', views_genus.GenusViews.genus_detail, name='genus_detail'),
]
