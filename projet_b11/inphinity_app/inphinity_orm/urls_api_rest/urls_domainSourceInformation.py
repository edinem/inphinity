from django.urls import path, include

from ..views import views_domainSourceInformation


urlpatterns = [
    path('', views_domainSourceInformation.DomainSourceInformationView.DomainSourceInformation_list),
    path('<int:pk>/', views_domainSourceInformation.DomainSourceInformationView.domainSourceInteractionPair_detail),
]
