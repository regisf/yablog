from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

try:
    from filebrowser.sites import site
except:
    pass
    
from django.contrib.sitemaps import Sitemap
from blog.models import Post

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.filter(Publish=True)

    def lastmod(self, obj):
        return obj.CreationDate

handler500 = 'blog.views.index'

urlpatterns = patterns('',
    # Uncomment for enabling maintenance mode
    #(r'^', 'blog.views.maintenance'),
    
    # Grappelli admin
#    url(r'^grappelli/', include('grappelli.urls')),
    
    # File Browser
#    url(r'^admin/filebrowser/', include(site.urls)),

    # Administration
    url(r'^admin/doc/',     include('django.contrib.admindocs.urls')),
    url(r'^admin/',         include(admin.site.urls)),

    url(r'^blog/',          include('blog.urls')),
    url(r'^$',              'blog.views.index',                 name="home"),
    
    #(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', 
    url(r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'blog':BlogSitemap}}),
    url(r'^robots\.txt', 'blog.views.robot'),
)

from django.conf import settings
import os
if settings.IS_LOCAL:
    from django.views.static import serve
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$',
            serve,
            dict(
                document_root = os.path.join(settings.PROJECT_PATH, 'site_media/'),
                show_indexes = True
            )
        ),
    )
