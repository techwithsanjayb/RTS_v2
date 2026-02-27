from django.urls import path
from . import views

abstract_urlpatterns = [
    path('user_login',views.user_login,name="user_login"),
    path('', views.home, name="home"),
    path('dashboard', views.dashboard, name="dashboard"),  
]