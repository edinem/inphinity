#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_lysisType


urlpatterns = [
    path('', views_lysisType.LysisTypeView.lysisType_list),
    path('<int:pk>/', views_lysisType.LysisTypeView.lysisType_detail),
]
