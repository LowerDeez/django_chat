from django.urls import re_path
from django.contrib.auth import views
from accounts.views import LoginView, RegisterView, UserView, UserEditView, \
    save_photo_user, delete_photo_user


urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', views.logout, {'next_page': 'login'}, name='logout'),
    re_path(r'^register/$', RegisterView.as_view(), name='register'),

    re_path(r'^user/(?P<pk>[0-9]+)/$', UserView.as_view(), name='user_view'),
    re_path(r'^user/(?P<pk>[0-9]+)/edit/$', UserEditView.as_view(), name='user_edit'),
    re_path(r'^save_photo_user/(?P<pk>[0-9]+)/$', save_photo_user, name='save_photo_user'),
    re_path(r'^delete_photo_user/(?P<pk>[0-9]+)/$', delete_photo_user, name='delete_photo_user'),
]
