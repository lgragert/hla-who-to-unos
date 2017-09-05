from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name="home"),
    url(r'^home_1', views.home_1, name="home_1"),
    url(r'^allele', views.allele, name="allele"),
    url(r'^lists', views.allele_list, name="lists"),
    url(r'^gl_string', views.gl_string, name="gl_string"),
    url(r'^codes', views.allele_codes, name="codes"),
    url(r'^convert/', views.convert, name="convert"),
    url(r'^convert_2/', views.convert_2, name="convert_2"),
    url(r'^convert_3/', views.convert_3, name="convert_3"),
    url(r'^convert_4/', views.convert_4, name="convert_4"),
    ]
