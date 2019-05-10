from django.urls import path, include

from ..views import views_baltimorClassification


urlpatterns = [
    path('', views_baltimorClassification.BaltimoreClassificationView.baltimoreClassification_list),
    path('<int:pk>/', views_baltimorClassification.BaltimoreClassificationView.baltimoreClassification_detail, name='baltimore_classification_detail'),
]
