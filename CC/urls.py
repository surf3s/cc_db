from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CC.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'CC_DB.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls),name='admin'),
    url(r'^populate_context/', 'CC_DB.views.populate_context', name='populate_context'),
    url(r'^populate_lithics/', 'CC_DB.views.populate_lithics', name='populate_lithics'),
    url(r'^populate_small_finds/', 'CC_DB.views.populate_small_finds', name='populate_small_finds'),
    url(r'^populate_photos/', 'CC_DB.views.populate_photos', name='populate_photos'),
    url(r'^populate_database/', 'CC_DB.views.populate_database', name='populate_database'),
    url(r'^populate_xyz/', 'CC_DB.views.populate_xyz', name='populate_xyz'),
    url(r'^populate_units/', 'CC_DB.views.populate_units', name='populate_units'),
    url(r'^debugger/', 'CC_DB.views.debugger', name='debugger'),
)
