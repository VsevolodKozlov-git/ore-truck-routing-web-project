from django.urls import path

from app import views

urlpatterns = [
    path('test', views.TestView.as_view(), name='test'),
    path('', views.RootView.as_view(), name='root')
]