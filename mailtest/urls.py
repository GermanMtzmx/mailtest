"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, re_path as path
from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from django.contrib.staticfiles import views

from .views import not_found


urlpatterns = [
    # Admin
    path(r'^admin/', admin.site.urls),

    # API v1
    path(r'^api/v1/', include('common.urls')),
    path(r'^api/v1/', include('accounts.urls')),

    # Media
    path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT}, name='media'),
]

# Statics
if settings.DEBUG:
    urlpatterns += [
        path(r'^static/(?P<path>.*)$', views.serve, name='static')]
else:
    urlpatterns += [path(r'^static/(?P<path>.*)$',
        serve, {'document_root': settings.STATIC_ROOT}, name='static')]

# 404 error
urlpatterns += [path(r'^', not_found, name='not-found')]
