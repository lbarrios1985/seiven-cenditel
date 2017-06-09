"""seiven URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from base import views as base_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', base_views.inicio, name='inicio'),
    url(r'^', include('base.urls')),
    url(r'economico/', include('economico.urls')),
    url(r'productivo/', include('productivo.urls')),
    url(r'^gestion-informacion/', include('gestion_informacion.urls')),
    url(r'^', include('usuario.urls')),
    url(r'^captcha/', include('captcha.urls')),
]
