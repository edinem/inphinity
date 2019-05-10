#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_cogInteractionPair


urlpatterns = [
    path('', views_cogInteractionPair.COGInterationPairView.cogInteractionPair_list),
    path('<int:pk>/', views_cogInteractionPair.COGInterationPairView.cogInteractionPair_detail),
]
