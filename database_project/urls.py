from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'database_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^forms/',include('online_forms.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
