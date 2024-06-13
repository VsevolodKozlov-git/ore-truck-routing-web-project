from django.urls import path

from app import views

urlpatterns = [
    path('', views.RootView.as_view(), name='root')
]