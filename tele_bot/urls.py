"""tele_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from oauth import views as oauthview
from django.contrib.auth.views import login
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', oauthview.index),
    url(r'^bot/', include('bot.urls')),
    url(r'^oauth2callback', oauthview.auth_return),
    url(r'^accounts/login/$', login,
                        {'template_name': 'login.html'}, name='login'),
]
