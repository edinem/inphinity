#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_pfamMethodScore


urlpatterns = [
    path('', views_pfamMethodScore.PFAMMethodScoreView.pfamMethodScore_list),
    path('<int:pk>/', views_pfamMethodScore.PFAMMethodScoreView.pfamMethodScore_detail),
]
