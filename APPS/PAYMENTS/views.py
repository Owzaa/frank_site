from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.urls import reverse

from datetime import date
import uuid
import json

from paypal.standard.forms import PayPalPaymentsForm

from .models import PaymentMode, PaymentGateway, PaymentMethod
from APPS.STORE.models import Order

# Dashboard view for payments
@login_required
def payments_dashboard(request):
    """Dashboard view showing payment history and saved payment methods"""
    user_payments = PaymentMode.objects.filter(user=request.user).order_by('-created_at')[:10]
    payment_methods = PaymentMethod.objects.filter(user=request.user)
    
    context = {
        'year': date.today().year,
        'payments': user_payments,
        'payment_methods': payment_methods,
    }
    return render(request, 'apps/payments/dashboard.html', context)

# Process a payment
@login_required
@transaction.atomic
def process_payment(request, order_id=None):
    """Process a payment for an order"""
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('shop')
    
    # Get the order if order_id is provided
    order = None
    if order_id:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Get payment details from the form
    payment_method = request.POST.get('payment_method')
    
    # Handle different payment methods
    if payment_method == 'credit_card':
        return process_credit_card_payment(request, order)
    elif payment_method == 'paypal':
        return process_paypal_payment(request, order)
    else:
        messages.error(request, "Invalid payment method selected.")
        if order:
            return redirect('payment', order_id=order.id)
        return redirect('shop')

@login_required
@transaction.atomic
def process_credit_card_payment(request, order):
    """Process a credit card payment"""
    # Check if using a saved card or a new one
    card_id = request.POST.get('card_id')
    
    if card_id and card_id != '':
        # Using a saved card
        payment_method = get_object_or_404(PaymentMethod, id=card_id, user=request.user)
        card_details = payment_method.details
    else:
        # Using a new card
        card_holder = request.POST.get('card_holder')
        card_number = request.POST.get('card_number')
        expiry_month = request.POST.get('expiry_month')
        expiry_year = request.POST.get('expiry_year')
        cvv = request.POST.get('cvv')  # Don't store in production
        
        # Validate card details
        if not all([card_holder, card_number, expiry_month, expiry_year, cvv]):
            messages.error(request, "Please fill in all card details.")
            return redirect('payment', order_id=order.id)
        
        # Save card if requested
        save_card = request.POST.get('save_card') == 'on'
        
        if save_card:
            # Create a new payment method
            card_details = {
                'card_holder': card_holder,
                'card_number': card_number,
                'expiry_month': expiry_month,
                'expiry_year': expiry_year,
            }
            
            payment_method = PaymentMethod.objects.create(
                user=request.user,
                method_type='credit_card',
                name=f"{card_holder}'s Card",
                details=card_details,
                is_default=not PaymentMethod.objects.filter(user=request.user).exists(),
                last_used=timezone.now()
            )
        else:
            # Just use the card details without saving
            card_details = {
                'card_holder': card_holder,
                'card_number': card_number,
                'expiry_month': expiry_month,
                'expiry_year': expiry_year,
            }
    
    # In a real application, you would integrate with a payment gateway here
    # For this example, we'll simulate a successful payment
    
    # Get or create a credit card payment gateway
    gateway, _ = PaymentGateway.objects.get_or_create(
        gateway_type='credit_card',
        defaults={
            'name': 'Credit Card Processor',
            'is_active': True
        }
    )
    
    # Create a payment record
    transaction_id = f"CC-{uuid.uuid4().hex[:12].upper()}"
    payment = PaymentMode.objects.create(
        user=request.user,
        order_id=str(order.id),
        amount=order.total_price,
        gateway=gateway,
        payment_method='credit_card',
        transaction_id=transaction_id,
        transaction_data={
            'card_last4': card_details['card_number'][-4:],
            'card_holder': card_details['card_holder'],
            'expiry': f"{card_details['expiry_month']}/{card_details['expiry_year']}"
        }
    )
    
    # Mark payment as completed
    payment.complete_payment(transaction_id)
    
    # Update order status
    order.update_status('processing')
    
    messages.success(request, "Payment processed successfully!")
    return redirect('order_confirmation', order_id=order.id)

@login_required
def process_paypal_payment(request, order):
    """Initiate a PayPal payment"""
    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": f"{order.total_price:.2f}",
        "item_name": f"Order {order.id}",
        "invoice": f"{order.id}-{uuid.uuid4().hex[:8]}",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('paypal_return', kwargs={'order_id': order.id})),
        "cancel_return": request.build_absolute_uri(reverse('paypal_cancel', kwargs={'order_id': order.id})),
        "custom": order.id,  # Custom data you want to pass to PayPal
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"order": order, "form": form}
    return render(request, "apps/payments/paypal_form.html", context)



@login_required
@transaction.atomic
def paypal_return(request, order_id):
    """Handle successful PayPal payment return"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # In a real application, you would verify the payment with PayPal's IPN here
    # For this example, we'll assume it's successful
    
    # Get or create a PayPal payment gateway
    gateway, _ = PaymentGateway.objects.get_or_create(
        gateway_type='paypal',
        defaults={
            'name': 'PayPal',
            'is_active': True
        }
    )
    
    # Create a payment record (if not already created by IPN)
    payment, created = PaymentMode.objects.get_or_create(
        user=request.user,
        order_id=str(order.id),
        gateway=gateway,
        payment_method='paypal',
        defaults={
            'amount': order.total_price,
            'status': 'pending', # Will be updated by IPN or manually here
            'transaction_id': f"PP-RETURN-{uuid.uuid4().hex[:8]}"
        }
    )
    
    # Mark payment as completed
    payment.complete_payment(payment.transaction_id)
    
    # Update order status
    order.update_status('processing')
    
    messages.success(request, "PayPal payment completed successfully!")
    return redirect('order_confirmation', order_id=order.id)

@login_required
def paypal_cancel(request, order_id):
    """Handle cancelled PayPal payment"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Get or create a PayPal payment gateway
    gateway, _ = PaymentGateway.objects.get_or_create(
        gateway_type='paypal',
        defaults={
            'name': 'PayPal',
            'is_active': True
        }
    )
    
    # Create a payment record (if not already created by IPN)
    payment, created = PaymentMode.objects.get_or_create(
        user=request.user,
        order_id=str(order.id),
        gateway=gateway,
        payment_method='paypal',
        defaults={
            'amount': order.total_price,
            'status': 'failed', # Will be updated by IPN or manually here
            'transaction_id': f"PP-CANCEL-{uuid.uuid4().hex[:8]}"
        }
    )
    
    # Mark payment as failed
    payment.fail_payment("Payment cancelled by user")
    
    messages.warning(request, "PayPal payment was cancelled.")
    return redirect('payment', order_id=order.id)

@login_required
def payment_methods(request):
    """View and manage saved payment methods"""
    payment_methods = PaymentMethod.objects.filter(user=request.user)
    
    context = {
        'payment_methods': payment_methods,
    }
    
    return render(request, 'apps/payments/payment_methods.html', context)

@login_required
def add_payment_method(request):
    """Add a new payment method"""
    if request.method == 'POST':
        method_type = request.POST.get('method_type')
        name = request.POST.get('name')
        
        if method_type == 'credit_card':
            card_holder = request.POST.get('card_holder')
            card_number = request.POST.get('card_number')
            expiry_month = request.POST.get('expiry_month')
            expiry_year = request.POST.get('expiry_year')
            cvv = request.POST.get('cvv')  # Don't store in production
            
            # Validate card details
            if not all([card_holder, card_number, expiry_month, expiry_year, cvv]):
                messages.error(request, "Please fill in all card details.")
                return redirect('payment_methods')
            
            # Create a new payment method
            card_details = {
                'card_holder': card_holder,
                'card_number': card_number,
                'expiry_month': expiry_month,
                'expiry_year': expiry_year,
            }
            
            PaymentMethod.objects.create(
                user=request.user,
                method_type='credit_card',
                name=name or f"{card_holder}'s Card",
                details=card_details,
                is_default=not PaymentMethod.objects.filter(user=request.user).exists()
            )
            
            messages.success(request, "Credit card added successfully.")
        
        return redirect('payment_methods')
    
    return render(request, 'apps/payments/add_payment_method.html')

@login_required
def delete_payment_method(request, method_id):
    """Delete a payment method"""
    payment_method = get_object_or_404(PaymentMethod, id=method_id, user=request.user)
    
    if request.method == 'POST':
        payment_method.delete()
        messages.success(request, "Payment method deleted successfully.")
    
    return redirect('payment_methods')

@login_required
def set_default_payment_method(request, method_id):
    """Set a payment method as default"""
    payment_method = get_object_or_404(PaymentMethod, id=method_id, user=request.user)
    
    if request.method == 'POST':
        payment_method.is_default = True
        payment_method.save()
        messages.success(request, "Default payment method updated.")
    
    return redirect('payment_methods')

def payments(request):
    year = date.today().year
    return render(request, 'apps/payments/payment.html',{'year':year})