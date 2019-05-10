#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_interactionValidity


urlpatterns = [
    path('', views_interactionValidity.InteractionValidityView.interactionValidity_list),
    path('<int:pk>/', views_interactionValidity.InteractionValidityView.interactionValidity_detail),
]
