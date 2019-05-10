from django.urls import path, include

from ..views import views_sourceData


urlpatterns = [
    path('', views_sourceData.SourceDataView.sourceData_list),
    path('<int:pk>/', views_sourceData.SourceDataView.sourceData_detail, name='person_responsible_detail'),
]
