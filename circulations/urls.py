from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.circulations, name='circulations'),

    url(r'^issue/$', views.add_circulation, name='add_circulation'),

    url(r'^issue/confirm/$', views.add_circulation_confirm, name='add_circulation_confirm'),

    url(r'^return/$', views.return_circulation, name='return_circulation'),

    url(r'^return/confirm/$', views.return_circulation_confirm, name='return_circulation_confirm'),
]
