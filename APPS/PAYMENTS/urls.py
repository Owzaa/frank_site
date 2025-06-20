from django.urls import path
from . import views

urlpatterns = [
    # Legacy URL for backward compatibility
    path('payments/', views.payments, name='payments'),
    
    # Dashboard and payment management
    path('dashboard/', views.payments_dashboard, name='payments_dashboard'),
    path('methods/', views.payment_methods, name='payment_methods'),
    path('methods/add/', views.add_payment_method, name='add_payment_method'),
    path('methods/<int:method_id>/delete/', views.delete_payment_method, name='delete_payment_method'),
    path('methods/<int:method_id>/default/', views.set_default_payment_method, name='set_default_payment_method'),
    
    # Payment processing
    path('process/<int:order_id>/', views.process_payment, name='process_payment'),
    path('paypal/redirect/<int:payment_id>/', views.paypal_redirect, name='paypal_redirect'),
    path('paypal/return/<int:payment_id>/', views.paypal_return, name='paypal_return'),
    path('paypal/cancel/<int:payment_id>/', views.paypal_cancel, name='paypal_cancel'),
]