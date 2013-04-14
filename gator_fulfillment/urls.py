from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gator_fulfillment.views.home', name='home'),
    # url(r'^gator_fulfillment/', include('gator_fulfillment.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', redirect_to, {'url': '/admin/', 'permanent': True}),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^orders/label/(?P<order_id>\d+)/$', 'orders.views.label'),
    url(r'^orders/packing_label/(?P<order_id>\d+)/$', 'orders.views.packing_label'),
    url(r'^orders/hardware_order_form/(?P<order_id>\d+)/$', 'orders.views.hardware_order_form')
)

# urls for statis files
urlpatterns += patterns('',
    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
