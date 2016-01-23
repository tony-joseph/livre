"""livre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts import views as accounts_views
from index import views as index_views
from items import urls as items_urls
from accounts import urls as accounts_urls
from circulations import urls as circulations_urls
from search import urls as search_urls


urlpatterns = [
    url(r'^$', index_views.index, name='index'),

    url(r'^accounts/login/$', accounts_views.login_user, name='login'),

    url(r'^accounts/logout/$', auth_views.logout, {
        'template_name': 'accounts/logout.html',
    }, name='logout'),

    url(r'^accounts/register/$', accounts_views.register, name='register'),

    url(r'^accounts/password-change/$', auth_views.password_change, {
        'template_name': 'accounts/password-change.html',
    }, name='password_change'),

    url(r'^accounts/password-change-done/$', auth_views.password_change_done, {
        'template_name': 'accounts/password-change-done.html',
    }, name='password_change_done'),

    url(r'^accounts/password-reset/$', auth_views.password_reset, {
        'template_name': 'accounts/password-reset.html',
        'email_template_name': 'email/password-reset.html',
        'subject_template_name': 'email/password-reset-subject.html',
    }, name='password_reset'),

    url(r'^accounts/password-reset-done/$', auth_views.password_reset_done, {
        'template_name': 'accounts/password-reset-done.html',
    }, name='password_reset_done'),

    url(r'^accounts/password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, {
        'template_name': 'accounts/password-reset-confirm.html',
    }, name='password_reset_confirm'),

    url(r'^accounts/password-reset-complete/$', auth_views.password_reset_complete, {
        'template_name': 'accounts/password-reset-complete.html',
    }, name='password_reset_complete'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^items/', include(items_urls, namespace='items')),

    url(r'^accounts/', include(accounts_urls, namespace='accounts')),

    url(r'^circulations/', include(circulations_urls, namespace='circulations')),

    url(r'^search/', include(search_urls, namespace='search')),
]
