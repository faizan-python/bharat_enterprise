from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^vendor/get/$', 'vehicle.views.get_vendor_vehicle',
        name='get_vendor_vehicle'),
)
