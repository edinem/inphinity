#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_domainMethodScore


urlpatterns = [
    path('', views_domainMethodScore.DomainMethodScoreView.domainMethodScore_list),
    path('<int:pk>/', views_domainMethodScore.DomainMethodScoreView.domainMethodScore_detail),
]
