from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'CC_DB.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls),name='admin'),
    url(r'^populate_database/', 'CC_DB.views.populate_database', name='populate_database'),
)
