from django.conf.urls import url

from .views import home, login_view, logout_view, subscribed_user, send_notification

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^subscribe_user/$', subscribed_user, name='sUser'),
    url(r'^send_notification/', send_notification, name='SN'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
]
