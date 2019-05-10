#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_ppiInteractionSource


urlpatterns = [
    path('', views_ppiInteractionSource.PPIInteractionSourceView.ppiInteractionSource_list),
    path('<int:pk>/', views_ppiInteractionSource.PPIInteractionSourceView.ppiInteractionSource_detail),
]
