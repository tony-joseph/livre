from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),

    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),

    url(r'^users/$', views.list_users, name='list_users'),

    url(r'^users/add/$', views.add_user, name='add_user'),

    url(r'^users/(?P<username>[-a-zA-Z0-9_]+)/$', views.view_user_profile, name='view_user_profile'),

    url(r'^users/(?P<username>[-a-zA-Z0-9_]+)/remove/$', views.remove_user, name='remove_user'),

    url(r'^users/(?P<username>[-a-zA-Z0-9_]+)/change-staff-status/$', views.change_staff_status,
        name='change_staff_status'),

    url(r'^users/(?P<username>[-a-zA-Z0-9_]+)/change-admin-status/$', views.change_admin_status,
        name='change_admin_status'),

    url(r'^my-books/$', views.my_books, name='my_books'),
]
