#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_ppi


urlpatterns = [
    path('', views_ppi.PPIView.ppi_list),
    path('<int:pk>/', views_ppi.PPIView.ppi_detail),
]
