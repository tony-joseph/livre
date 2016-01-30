from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^categories/$', views.list_categories, name='list_categories'),

    url(r'^categories/add/$', views.add_category, name='add_category'),

    url(r'^categories/(?P<slug>[-a-zA-Z0-9_]+)/$', views.view_category, name='view_category'),

    url(r'^categories/(?P<slug>[-a-zA-Z0-9_]+)/edit/$', views.edit_category, name='edit_category'),

    url(r'^categories/(?P<slug>[-a-zA-Z0-9_]+)/delete/$', views.delete_category, name='delete_category'),

    url(r'^categories/(?P<slug>[-a-zA-Z0-9_]+)/books/$', views.category_books, name='category_books'),

    url(r'^languages/$', views.list_languages, name='list_languages'),

    url(r'^languages/add/$', views.add_language, name='add_language'),

    url(r'^languages/(?P<slug>[-a-zA-Z0-9_]+)/$', views.view_language, name='view_language'),

    url(r'^languages/(?P<slug>[-a-zA-Z0-9_]+)/edit/$', views.edit_language, name='edit_language'),

    url(r'^languages/(?P<slug>[-a-zA-Z0-9_]+)/delete/$', views.delete_language, name='delete_language'),

    url(r'^languages/(?P<slug>[-a-zA-Z0-9_]+)/books/$', views.language_books, name='language_books'),

    url(r'^books/$', views.list_book_details, name='list_book_details'),

    url(r'^books/add/$', views.add_book_detail, name='add_book_detail'),

    url(r'^books/(?P<id>[0-9]+)/$', views.view_book_detail, name='view_book_detail'),

    url(r'^books/(?P<id>[0-9]+)/edit/$', views.edit_book_detail, name='edit_book_detail'),

    url(r'^books/(?P<id>[0-9]+)/delete/$', views.delete_book_detail, name='delete_book_detail'),

    url(r'^books/(?P<book_id>[0-9]+)/copy/add/$', views.add_book_copy, name='add_book_copy'),

    url(r'^books/(?P<book_id>[0-9]+)/copy/(?P<copy_id>[0-9]+)/$', views.view_book_copy, name='view_book_copy'),

    url(r'^books/(?P<book_id>[0-9]+)/copy/(?P<copy_id>[0-9]+)/edit/$', views.edit_book_copy, name='edit_book_copy'),

    url(r'^books/(?P<book_id>[0-9]+)/copy/(?P<copy_id>[0-9]+)/delete/$', views.delete_book_copy,
        name='delete_book_copy'),

    url(r'^periodicals/$', views.list_periodicals, name='list_periodicals'),

    url(r'^periodicals/add/$', views.add_periodical, name='add_periodical'),

    url(r'^periodicals/(?P<id>[0-9]+)/$', views.view_periodical, name='view_periodical'),

    url(r'^periodicals/(?P<id>[0-9]+)/edit/$', views.edit_periodical, name='edit_periodical'),

    url(r'^periodicals/(?P<id>[0-9]+)/delete/$', views.delete_periodical, name='delete_periodical'),

    url(r'^periodicals/(?P<periodical_id>[0-9]+)/issues/$', views.list_periodical_issues, name='list_periodical_issues'),

    url(r'^periodicals/(?P<periodical_id>[0-9]+)/issues/add/$', views.add_periodical_issue, name='add_periodical_issue'),

    url(r'^periodicals/(?P<periodical_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/$', views.view_periodical_issue,
        name='view_periodical_issue'),

    url(r'^periodicals/(?P<periodical_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/edit/$', views.edit_periodical_issue,
        name='edit_periodical_issue'),

    url(r'^periodicals/(?P<periodical_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/delete/$', views.delete_periodical_issue,
        name='delete_periodical_issue'),
]
