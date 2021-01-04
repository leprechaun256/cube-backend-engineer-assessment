from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^assessment/', include('django_business_rules.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^cube-server/', include('cube.urls')),
]