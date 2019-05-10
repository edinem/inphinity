#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_cog


urlpatterns = [
    path('', views_cog.COGView.cog_list),
    path('<int:pk>/', views_cog.COGView.cog_detail),
]
