#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_sourceCog


urlpatterns = [
    path('', views_sourceCog.SourceCogView.sourceCog_list),
    path('<int:pk>/', views_sourceCog.SourceCogView.sourceCog_detail),
]
