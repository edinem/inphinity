#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_ppiCogScore


urlpatterns = [
    path('', views_ppiCogScore.PPICOGcoreView.ppiCogScore_list),
    path('<int:pk>/', views_ppiCogScore.PPICOGcoreView.ppiCogScore_detail),
]
