"""myDjangoProject URL Configuration

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
from . import view
from . import search
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view.index),
    url(r'^home$', view.home),
    url(r'^run$', view.run),
    url(r'^war$', view.getwar),
    url(r'^mv$', view.move),
    url(r'^rwar$', view.getRwar),
    url(r'^stop$', view.stop),
    url(r'^start$', view.start),
    url(r'^ps$', view.ps),
    url(r'^log$', view.log),
    url(r'^search-form$', search.search_form),
    url(r'^static/(?P<path>.*)$',serve,{"document_root":settings.STATICFILES_DIRS}),
] 

