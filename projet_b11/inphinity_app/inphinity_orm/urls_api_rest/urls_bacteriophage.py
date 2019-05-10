from django.urls import path, re_path, include

from ..views import views_bacteriophage


urlpatterns = [
    path('', views_bacteriophage.BacteriophageViews.bacteriophage_list),
    path('<int:pk>/', views_bacteriophage.BacteriophageViews.bacteriophage_detail),
    re_path(r'^design/(?P<designation>[\w._]{1,200})/exists/$', views_bacteriophage.BacteriophageViews.bacteriumDesignExists, name='bacteriumDesignExists'),
    re_path(r'^design/(?P<designation>[\w._]{1,200})/$', views_bacteriophage.BacteriophageViews.bacteriophageByDesignation, name='bacteriophageByDesignation'),
	re_path(r'^accnumber/(?P<accnumber>[\w.]{1,40})/$', views_bacteriophage.BacteriophageViews.bacteriophageByAcc, name='bacteriophageByAcc'),

]
