from django.urls import path
from . import views

app_name = "resolver"

urlpatterns = [
    path('dashboard/', views.resolver_dashboard, name='dashboard'),
]