#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_domainInteractionScore


urlpatterns = [
    path('', views_domainInteractionScore.DomainInteractionScoreView.domainInteractionScore_list),
    path('<int:pk>/', views_domainInteractionScore.DomainInteractionScoreView.domainInteractionScore_detail),
]
