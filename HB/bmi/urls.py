from . import views
from . import views_auth
from django.urls import path

urlpatterns = [
    path('login/', views_auth.login),
    path('signup/', views_auth.signup),
    path('user/', views.get_user),
    path('create_bmi/', views.create_bmi),
    path('get_bmi/', views.get_bmi),
    path('delete/', views.user_delete),
    path('update/', views.user_update),
    path('delete_bmi/', views.delete_bmi),
]
