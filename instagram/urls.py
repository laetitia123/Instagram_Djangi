"""tribune URL Configuration

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
from django.contrib.auth import views 
from django.contrib.auth.models import User

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'',include('photos.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # url(r'^accounts/login/$', include('news.urls')),
    url(r'^logout/$', views.logout, {"next_page": '/'}), 
    url(r'^tinymce/', include('tinymce.urls')),

] 
# We first import the views module from the django.contrib.auth module. Then we create a new URLconf. We provide the keyword argument next_page to define the page to go to after the user is logged out.
