#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_ppiSource


urlpatterns = [
    path('', views_ppiSource.PPISourceView.ppiSource_list),
    path('<int:pk>/', views_ppiSource.PPISourceView.ppiSource_detail),
]
