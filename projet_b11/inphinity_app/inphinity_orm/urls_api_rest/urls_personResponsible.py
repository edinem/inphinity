from django.urls import path, include

from ..views import views_personResponsible


urlpatterns = [
    path('', views_personResponsible.PersonResponsibleView.personeResponsible_list),
    path('<int:pk>/', views_personResponsible.PersonResponsibleView.personeResponsible_detail, name='source_data_detail'),
]
