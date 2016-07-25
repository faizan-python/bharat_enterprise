from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^advance/$', 'payment.views.advance_payment',
        name='advance_payment'),
    url(r'^advance/pay/$', 'payment.views.advance_payment_pay',
        name='advance_payment_pay'),
    )
