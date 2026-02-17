
 
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name="home"),
    path('login_view', views.login_view, name="login_view"),
    path('user_logout', views.user_logout , name='user_logout'),
    path('agent_dashboard', views.agent_dashboard, name="agent_dashboard"),
    path('user_dashboard', views.user_dashboard, name="user_dashboard"),
    path('administrator_dashboard', views.administrator_dashboard, name="administrator_dashboard"),    
]
