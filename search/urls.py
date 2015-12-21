from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^books/$', views.search_books, name='search_books'),

    url(r'^periodicals/$', views.search_periodicals, name='search_periodicals'),
]
