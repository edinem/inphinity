#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_ppiPfamScore


urlpatterns = [
    path('', views_ppiPfamScore.PPIPFAMScoreView.ppiPfamScore_list),
    path('<int:pk>/', views_ppiPfamScore.PPIPFAMScoreView.ppiPfamScore_detail),
]
