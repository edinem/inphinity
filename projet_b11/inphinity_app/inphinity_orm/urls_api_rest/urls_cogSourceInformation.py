#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_cogSourceInformation


urlpatterns = [
    path('', views_cogSourceInformation.COGSourceInformationView.cogSourceInformation_list),
    path('<int:pk>/', views_cogSourceInformation.COGSourceInformationView.cogSourceInformation_detail),
]
