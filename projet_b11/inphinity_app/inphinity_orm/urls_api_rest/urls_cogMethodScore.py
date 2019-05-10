#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_cogMethodScore


urlpatterns = [
    path('', views_cogMethodScore.COGMethodScoreView.cogMethodScore_list),
    path('<int:pk>/', views_cogMethodScore.COGMethodScoreView.cogMethodScore_detail),
]
