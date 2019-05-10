#from rest_framework.urlpatterns import format_suffix_patterns


from ..views import views_family


urlpatterns = [
    path('', views_family.FamilyView.family_list),
    path('<int:pk>/', views_family.FamilyView.family_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
