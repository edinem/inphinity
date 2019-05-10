#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_cogInteractionSource


urlpatterns = [
    path('', views_cogInteractionSource.COGInteractionSourceView.cogInteractionSource_list),
    path('<int:pk>/', views_cogInteractionSource.COGInteractionSourceView.cogInteractionSource_detail),
]
