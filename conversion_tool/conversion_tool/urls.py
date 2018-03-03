from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from . import views
from . import views_a
from . import views_al
from . import views_gl
from . import views_ac
from . import views_reverse
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Web services interface information for ALLAN: IMGT/HLA ALLele to UNOS ANtigen conversion tool')


urlpatterns = [
    url(r'^tool_services', schema_view, name="tool_services"),
    url(r'^gragertlabpersonel/', admin.site.urls),
    url(r'^$', views.home, name="home"),
    url(r'^home_1', views.home_1, name="home_1"),
    url(r'^license', views.license, name="license"),
    url(r'^allele', views.allele, name="allele"),
    url(r'^lists', views.allele_list, name="lists"),
    url(r'^gl_string', views.gl_string, name="gl_string"),
    url(r'^codes', views.allele_codes, name="codes"),
    url(r'^convert/', views.convert, name="convert"),
    url(r'^convert_2/', views.convert_2, name="convert_2"),
    url(r'^convert_3/', views.convert_3, name="convert_3"),
    url(r'^convert_4/', views.convert_4, name="convert_4"),
    url(r'^reverse/', views.reverse, name="reverse"),
    url(r'^convert_5/', views.convert_5, name="convert_5"),
    url(r'^single_allele/', views_a.AlleleApiView.as_view()), #schema_view),
    url(r'^array/', views_al.AlleleListApiView.as_view()),
    url(r'^gls/', views_gl.GLstringApiView.as_view()),
    url(r'^macs/', views_ac.AlleleCodesApiView.as_view()),
    url(r'^reverse_mapping/', views_reverse.AlleleMappingApiView.as_view()),
    ]
