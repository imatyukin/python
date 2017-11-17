"""Определяет схемы URL для learning_logs."""

from django.conf.urls import url

from . import views

urlpatterns = [
    # Домашняя страница
    url(r'^$', views.index, name='index'),
]