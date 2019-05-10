#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from ..views import views_domainInteractionPair


urlpatterns = [
    path('', views_domainInteractionPair.DomainInterationsPairView.domainInteractionPair_list),
    path('<int:pk>/', views_domainInteractionPair.DomainInterationsPairView.domainInteractionPair_detail),
    path('ddi_existence/<slug:pfam_a>/<slug:pfam_b>/', views_domainInteractionPair.DomainInterationsPairView.ddiPairExists),
]
