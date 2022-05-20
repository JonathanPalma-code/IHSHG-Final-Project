from django.urls import URLPattern, path

from . import views

# app_name = 'report'

urlpatterns = [
    path('', views.dashboard, name='dashboard')
]