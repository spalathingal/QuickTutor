from django.urls import path

from . import views

urlpatterns = [
    path('about', views.about, name='about'),
    path('FAQ', views.FAQ, name='FAQ'),
]