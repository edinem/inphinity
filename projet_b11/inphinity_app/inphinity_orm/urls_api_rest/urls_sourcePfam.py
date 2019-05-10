#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_sourcePfam


urlpatterns = [
    path('', views_sourcePfam.SourcePFAMView.sourcePfam_list),
    path('<int:pk>/', views_sourcePfam.SourcePFAMView.sourcePfam_detail),
]
