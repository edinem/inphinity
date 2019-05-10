#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_levelInteraction


urlpatterns = [
    path('', views_levelInteraction.LevelInteractionView.levelInteraction_list),
    path('<int:pk>/', views_levelInteraction.LevelInteractionView.interactionValidity_detail),
]
