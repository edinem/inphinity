from django.urls import path, include

from ..views import views_domainInteractionSource


urlpatterns = [
    path('', views_domainInteractionSource.DomainInformationSourceView.DomainSourceInformation_list),
    path('<int:pk>/', views_domainInteractionSource.DomainInformationSourceView.domainInformationSource_detail),
    path('ddi_info_source_existence/<int:id_ddi>/<int:id_source>/', views_domainInteractionSource.DomainInformationSourceView.ddiPairSourceExists),
]
