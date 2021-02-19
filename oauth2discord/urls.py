from django.contrib import admin
from django.urls import path
from discordlogin.views import (indexView, discordLoginView)

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', indexView.as_view(), name='index'),
    path('oauth2/login/', discordLoginView.as_view(), name='oauth2-login')
]