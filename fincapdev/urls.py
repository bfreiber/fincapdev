from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fincapdev.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'fincapdev.views.landing', name='landing'),
    url(r'^dashboard$', 'fincapdev.views.dashboard', name='dashboard'),
    url(r'^network_view/$', 'fincapdev.views.network_view', name='network_view'),
    url(r'^network_view/(?P<pool_id>\d+)/$', 'fincapdev.views.network_view', name='network_view'),
    #Linkedin
    url(r'^linkedinauthentication$', 'fincapdev.views.linkedinauthentication', name='linkedinauthentication'),
    #Stripe
    url(r'^stripepayment/$', 'fincapdev.views.stripepayment', name='stripepayment'),

    url(r'^admin/', include(admin.site.urls)),
)
