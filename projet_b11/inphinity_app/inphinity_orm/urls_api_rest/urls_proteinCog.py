#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_proteinCog


urlpatterns = [
    path('', views_proteinCog.ProteinCogView.proteinCog_list),
    path('<int:pk>/', views_proteinCog.ProteinCogView.proteinCog_detail),
]
