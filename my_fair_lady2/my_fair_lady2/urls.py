from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(
        r'^$',
        'candidate_gatherer.views.landing_page',
        name='landing_page',
    ),

    url(
        r'^source_post$',
        'candidate_gatherer.views.source_post',
        name='source_post',
    ),

    url(
        r'^candidate_gatherer/(?P<source_id>[0-9]+)$',
        'candidate_gatherer.views.candidate_form',
        name='candidate_form',
    ),

    url(
        r'^candidate_gatherer/candidate_post$',
        'candidate_gatherer.views.candidate_post',
        name='candidate_post',
    ),

    url(
        r'^downloads/$',
        'candidate_gatherer.views.downloads',
        name='downloads',
    ),

    url(
        r'^download/(?P<source_id>[0-9]+)$',
        'candidate_gatherer.views.download',
        name='csv_download',
    ),

    # Examples:
    # url(r'^$', 'my_fair_lady2.views.home', name='home'),
    # url(r'^my_fair_lady2/', include('my_fair_lady2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # XXX: Change default resource name for security
    url(r'^the_best_admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # XXX: Change default resource name for security
    url(r'^the_best_admin/', include(admin.site.urls)),
    
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
)

# Uncomment the next line to serve media files in dev.
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
