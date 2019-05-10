from django.urls import path, include
from django.contrib.auth import urls
from . import views_score

# Tuto pour faire site web de consultation API

urlpatterns = [
    path('index/', views_score.scores_index, name='scores_index'),
    path('login/', views_score.log_user, name="log_user"),
    path('logout/', views_score.user_logout, name="user_logout"),
    path('generate/', views_score.generate_ds, name='generate_ds'),
    path('threshold/',views_score.generate_ds_thresholds, name="generate_ds_thresholds"),
    path('ds/',views_score.datasets, name="datasets"),
    path('ds/<str:file>/', views_score.ds_download, name="ds_download")

    # path('family/<int:fam_id>/', views_site.family_detail, name='family_detail'),
    # path('family/new/', views_site.family_new, name='family_new'),
]
