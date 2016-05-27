from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.post_list),  # first page with all post
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),  # page with a post detail
    url(r'^post/new/$', views.post_new, name='post_new'),  # insert new post
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),  # edit a post
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),  # list post without publish
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),  # publish a post in the draft list
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),  # remove a post
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),  # add comment to post
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),  # approve a comment as admin user
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),  # delete a comment as admin user
    url(r'^register/$', views.add_user, name='add_user'),  # insert new post
    url(r'^list/$', views.list, name='list'),  # cargar foto de usuario
    url(r'^list/(?P<pk>\d+)/remove/$', views.photo_remove, name='photo_remove'),  # delete a comment as admin user
    url(r'^profile/$', views.view_user_profile, name='view_user_profile'),  # views.view_user_profile es el método en views.py
]
