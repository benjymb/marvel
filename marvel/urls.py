"""untitled URL Configuration

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
from django.conf.urls import url
from django.contrib import admin

from demo import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^search$', views.QueryCharactersView.as_view(), name='search'),
    url(r'^character$', views.CharacterView.as_view(), name='character'),
    url(r'^most-popular$', views.MostPopularView.as_view(), name='most-popular'),
    url(r'^recent', views.RecentView.as_view(), name='recent'),
]
