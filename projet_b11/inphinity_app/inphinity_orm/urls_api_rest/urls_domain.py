from django.urls import path, include

from ..views import views_domain


urlpatterns = [
    path('', views_domain.DomainView.domain_list),
    path('<int:pk>/', views_domain.DomainView.domain_detail),
]
