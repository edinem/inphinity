from django.urls import path, re_path, include

from ..views import views_bacterium


urlpatterns = [
    path('', views_bacterium.BacteriumViews.bacterium_list),
    path('<int:pk>/', views_bacterium.BacteriumViews.bacterium_detail, name='bacterium_detail'),
    re_path(r'^accnumber/(?P<accnumber>[\w.]{1,40})/exists/$', views_bacterium.BacteriumViews.bacteriumAccExists, name='bacterium_acc'),
    re_path(r'^accnumber/(?P<accnumber>[\w.]{1,40})/$', views_bacterium.BacteriumViews.bacteriumByAcc, name='bacteriumByAcc'),
]
