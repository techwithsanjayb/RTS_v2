
 
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name="home"),
    path('login_view', views.login_view, name="login_view"),
    path('user_logout', views.user_logout , name='user_logout'),
    path('resolver_dashboard', views.resolver_dashboard, name="resolver_dashboard"),
    path('raiser_dashboard', views.raiser_dashboard, name="raiser_dashboard"),
    path('administrator_dashboard', views.administrator_dashboard, name="administrator_dashboard"),
]
