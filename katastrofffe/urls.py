"""katastrofffe URL Configuration

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
# from django.conf.urls import url
# from django.contrib import admin
#
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
# ]


from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import contact
from . import views
from django.utils.functional import curry
from django.views.defaults import *
from django.shortcuts import render_to_response
from django.template import RequestContext

admin.autodiscover()

handler404 = views.error404
handler500 = views.error500

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^portfolio/', include('portfolio.urls')),
    url(r'^events/',include('event.urls')),
    url(r'^about/', views.about, name='about'),
    url(r'^contact/', include('contact.urls')),
    url(r'^privacy_policy/',  views.privacy_policy, name='privacy_policy'),
    url(r'^terms_of_service/',  views.terms_of_service, name='terms_of_service'),
    url(r'^test/', views.test, name='test'),
    url(r'^dev/', views.dev, name='dev'),
    url(r'^googleb758d0ca397ee06d.html', views.google_verification, name='google_verification'),
    url(r'', views.index_page, name='index'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)

