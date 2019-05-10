#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_family


urlpatterns = [
    path('', views_family.FamilyView.family_list),
    path('<int:pk>/', views_family.FamilyView.family_detail),
]
