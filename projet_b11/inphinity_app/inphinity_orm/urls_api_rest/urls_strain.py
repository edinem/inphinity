from django.urls import path, re_path, include

from ..views import views_strain


urlpatterns = [
    path('', views_strain.StrainViews.strain_list),
    path('<int:pk>/', views_strain.StrainViews.strain_detail, name='strain_detail'),
    re_path(r'^existdesignstrain/(?P<designation>[\w._]{1,100})/(?P<fk_specie>[0-9]+)/$', views_strain.StrainViews.strainDesignSpecieExistes, name='strainDesignSpecieExistes'),
]
