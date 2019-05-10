#from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include, re_path

from ..views import views_couple


urlpatterns = [
    path('', views_couple.CoupleView.couple_list),
    path('<int:pk>/', views_couple.CoupleView.couple_detail),
	path('organismsid/<int:idBact>/<int:idPhage>/', views_couple.CoupleView.coupleDetailByIdBactIdPhage, name='coupleByOrganismsIds'),
]
