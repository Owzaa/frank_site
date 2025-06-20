from typing import Dict, List, Optional, Union, Any
from decimal import Decimal
from collections import defaultdict
import uuid
import time

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .models import Product, Category, Order, OrderItem, Payment, CreditCard, CartItem, ProductImage

def shop(request: HttpRequest) -> HttpResponse:
    """View function for the shop page that displays products grouped by category."""
    # Get query parameters
    search_query: str = request.GET.get('q', '')
    category_id: str = request.GET.get('category', '')
    sort_option: str = request.GET.get('sort', '')
    
    # Start with all products
    from django.db.models.query import QuerySet
    products_query: QuerySet[Product] = Product.objects.all().select_related('category')
    
    # Apply search filter if provided
    if search_query:
        products_query = products_query.filter(name__icontains=search_query) | \
                         products_query.filter(description__icontains=search_query)
    
    # Apply category filter if provided
    if category_id:
        try:
            products_query = products_query.filter(category_id=int(category_id))
        except ValueError:
            # Invalid category ID, ignore the filter
            pass
    
    # Apply sorting if provided
    if sort_option == 'price_asc':
        products_query = products_query.order_by('price')
    elif sort_option == 'price_desc':
        products_query = products_query.order_by('-price')
    elif sort_option == 'newest':
        products_query = products_query.order_by('-created_at')
    
    # Execute the query
    products: List[Product] = list(products_query)
    
    # Get all categories
    categories = Category.objects.all()
    
    # Group products by category for the category sliders
    products_by_category: defaultdict[Category, List[Product]] = defaultdict(list)
    for product in products:
        products_by_category[product.category].append(product)
    
    # Prepare data for template
    category_products: List[Dict[str, Any]] = []
    for category in categories:
        if category in products_by_category:
            category_products.append({'category': category, 'products': products_by_category[category][:8]})  # Limit to 8 products per category
    
    context: Dict[str, Any] = {
        'products': products,
        'categories': categories,
        'category_products': category_products
    }
    
    return render(request, 'shop/store.html', context)

def product_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """View function for displaying product details and related products."""
    product = get_object_or_404(Product, pk=pk)
    
    # Get related products from the same category, excluding the current product
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    
    context: Dict[str, Any] = {
        'product': product,
        'related_products': related_products
    }
    
    return render(request, 'products/product_detail.html', context)

# ---------- CART LOGIC USING DATABASE MODEL ----------
def _get_or_create_cart_id(request: HttpRequest) -> str:
    """Get the cart ID from session or create a new one"""
    if not request.session.get('cart_id'):
        request.session['cart_id'] = str(uuid.uuid4())
    return request.session['cart_id']

def add_to_cart(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """Add a product to the cart"""
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if we have enough stock
    if product.stock < quantity:
        messages.error(request, f"Sorry, we only have {product.stock} units of this product in stock.")
        return redirect('product_detail', pk=pk)
    
    if request.user.is_authenticated:
        # For logged-in users, use their account
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    else:
        # For anonymous users, use session ID
        session_id = _get_or_create_cart_id(request)
        cart_item, created = CartItem.objects.get_or_create(
            session_id=session_id,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('view_cart')

def remove_from_cart(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """Remove a product from the cart"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product=product).delete()
    else:
        session_id = _get_or_create_cart_id(request)
        CartItem.objects.filter(session_id=session_id, product=product).delete()
    
    messages.success(request, f"{product.name} removed from your cart.")
    return redirect('view_cart')

def update_cart(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """Update the quantity of a product in the cart"""
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        return remove_from_cart(request, pk)
    
    # Check if we have enough stock
    if product.stock < quantity:
        messages.error(request, f"Sorry, we only have {product.stock} units of this product in stock.")
        quantity = product.stock
    
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product=product)
        cart_item.quantity = quantity
        cart_item.save()
    else:
        session_id = _get_or_create_cart_id(request)
        cart_item = get_object_or_404(CartItem, session_id=session_id, product=product)
        cart_item.quantity = quantity
        cart_item.save()
    
    messages.success(request, "Cart updated successfully.")
    return redirect('view_cart')

def view_cart(request: HttpRequest) -> HttpResponse:
    """View the cart contents"""
    cart_items = []
    total = Decimal('0.00')
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    else:
        session_id = _get_or_create_cart_id(request)
        cart_items = CartItem.objects.filter(session_id=session_id).select_related('product')
    
    for item in cart_items:
        total += item.total
    
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def clear_cart(request: HttpRequest) -> HttpResponseRedirect:
    """Remove all items from the cart"""
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
    else:
        session_id = _get_or_create_cart_id(request)
        CartItem.objects.filter(session_id=session_id).delete()
    
    messages.success(request, "Your cart has been cleared.")
    return redirect('view_cart')

def merge_carts(request: HttpRequest) -> None:
    """Merge anonymous cart with user cart after login"""
    if 'cart_id' in request.session:
        session_id = request.session['cart_id']
        session_cart_items = CartItem.objects.filter(session_id=session_id)
        
        for item in session_cart_items:
            # Check if user already has this product in their cart
            user_cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=item.product,
                defaults={'quantity': item.quantity}
            )
            
            if not created:
                # If user already has this product, update quantity
                user_cart_item.quantity += item.quantity
                user_cart_item.save()
            
            # Delete the session cart item
            item.delete()
        
        # Clear the cart_id from session
        del request.session['cart_id']

# ---------- CHECKOUT AND PAYMENT LOGIC ----------
@login_required
@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    """Show checkout page with cart items and shipping/payment forms"""
    # Merge anonymous cart with user cart if needed
    merge_carts(request)
    
    # Get cart items
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Please add some products before checkout.")
        return redirect('view_cart')
    
    # Calculate total
    total = sum(item.total for item in cart_items)
    
    # Check stock availability
    for item in cart_items:
        if item.product.stock < item.quantity:
            messages.error(
                request, 
                f"Sorry, we only have {item.product.stock} units of {item.product.name} in stock. "
                f"Please update your cart."
            )
            return redirect('view_cart')
    
    # Get saved credit cards for the user
    saved_cards = CreditCard.objects.filter(user=request.user)
    
    return render(request, 'checkout/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'saved_cards': saved_cards
    })

@login_required
@transaction.atomic
def place_order(request: HttpRequest) -> HttpResponseRedirect:
    """Create a new order from the cart items"""
    if request.method != 'POST':
        return redirect('checkout')
    
    # Get cart items
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty. Please add some products before checkout.")
        return redirect('view_cart')
    
    # Check stock availability one more time
    for item in cart_items:
        if item.product.stock < item.quantity:
            messages.error(
                request, 
                f"Sorry, we only have {item.product.stock} units of {item.product.name} in stock. "
                f"Please update your cart."
            )
            return redirect('view_cart')
    
    with transaction.atomic():
        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=f"{request.user.first_name} {request.user.last_name}",
            email=request.user.email,
            phone=request.POST.get('phone', ''),
            shipping_address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            postal_code=request.POST.get('postal_code', ''),
            country=request.POST.get('country', ''),
            shipping_cost=Decimal('0.00'),  # Free shipping for now
            total_price=Decimal('0.00'),  # Will be calculated below
            status='pending',
            notes=request.POST.get('notes', '')
        )
        
        # Create order items and calculate total
        total_price = Decimal('0.00')
        for cart_item in cart_items:
            # Create OrderItem
            order_item = OrderItem.objects.create(
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Add to order
            order.items.add(order_item)
            total_price += order_item.get_total()
            
            # Update product stock
            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()
        
        # Update order total
        order.total_price = total_price
        order.save()
        
        # Clear cart
        cart_items.delete()
    
    messages.success(request, "Your order has been placed successfully!")
    
    # Redirect to payment page
    return redirect('payment', order_id=order.id)

@login_required
def payment(request: HttpRequest, order_id: int) -> HttpResponse:
    """Show payment page for an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if order is already paid
    if order.status == 'paid':
        messages.info(request, "This order has already been paid for.")
        return redirect('order_detail', order_id=order.id)
    
    # Get user's saved credit cards
    saved_cards = CreditCard.objects.filter(user=request.user)
    
    return render(request, 'checkout/payment.html', {
        'order': order,
        'saved_cards': saved_cards
    })

@login_required
@transaction.atomic
def process_payment(request: HttpRequest, order_id: int) -> HttpResponseRedirect:
    """Process payment for an order"""
    if request.method != 'POST':
        return redirect('payment', order_id=order_id)
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if order is already paid
    if order.status == 'paid':
        messages.info(request, 'This order has already been paid for.')
        return redirect('order_detail', order_id=order.id)
    
    # Get payment method
    payment_method = request.POST.get('payment_method')
    
    if payment_method == 'credit_card':
        # Get credit card details
        card_id = request.POST.get('card_id')
        
        if card_id:
            # Use saved card
            try:
                card = CreditCard.objects.get(id=card_id, user=request.user)
                
                # Check if card is expired
                if card.is_expired():
                    messages.error(request, 'This card has expired. Please use a different card.')
                    return redirect('payment', order_id=order.id)
                    
            except CreditCard.DoesNotExist:
                messages.error(request, 'Invalid credit card selected.')
                return redirect('payment', order_id=order.id)
        else:
            # Create new card
            card_number = request.POST.get('card_number')
            card_holder = request.POST.get('card_holder')
            expiry_month = request.POST.get('expiry_month')
            expiry_year = request.POST.get('expiry_year')
            cvv = request.POST.get('cvv')
            save_card = request.POST.get('save_card') == 'on'
            
            # Validate card details
            if not all([card_number, card_holder, expiry_month, expiry_year, cvv]):
                messages.error(request, 'Please fill in all credit card details.')
                return redirect('payment', order_id=order.id)
            
            # Create card object (but don't save to DB yet)
            card = CreditCard(
                user=request.user,
                card_number=card_number,
                card_holder=card_holder,
                expiry_month=expiry_month,
                expiry_year=expiry_year
            )
            
            # Check if card is expired
            if card.is_expired():
                messages.error(request, 'The card expiration date is invalid.')
                return redirect('payment', order_id=order.id)
            
            # Save card if requested (but don't save CVV)
            if save_card:
                card.save()
        
        # Create payment record
        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            payment_method='credit_card',
            status='processing'
        )
        
        try:
            # Process payment (this would connect to a payment gateway in production)
            # For demo purposes, we'll simulate a successful payment
            transaction_id = f'DEMO-{uuid.uuid4().hex[:8].upper()}'
            
            # Complete the payment using our enhanced model method
            payment.complete_payment(transaction_id=transaction_id)
            
            messages.success(request, 'Payment successful! Your order has been processed.')
            return redirect('order_detail', order_id=order.id)
            
        except Exception as e:
            # Handle payment failure
            payment.fail_payment(str(e))
            messages.error(request, f'Payment failed: {str(e)}')
            return redirect('payment', order_id=order.id)
    
    elif payment_method == 'paypal':
        # Implement PayPal payment logic here
        messages.info(request, 'PayPal payment is not implemented yet.')
        return redirect('payment', order_id=order.id)
    
    else:
        messages.error(request, 'Invalid payment method selected.')
        return redirect('payment', order_id=order.id)

def paypal_redirect(request: HttpRequest, payment_id: int) -> HttpResponse:
    """Handle PayPal payment redirection"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # In a real app, this would be a redirect to PayPal's website
    # For demo purposes, we'll just show a page with a button to simulate payment completion
    return render(request, 'checkout/paypal_redirect.html', {
        'payment': payment
    })

@login_required
def order_confirmation(request: HttpRequest, order_id: int) -> HttpResponse:
    """Show order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    return render(request, 'checkout/order_confirmation.html', {
        'order': order
    })

@login_required
def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    """Show detailed information about a specific order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Get payment information if available
    payment = None
    try:
        payment = Payment.objects.get(order=order)
    except Payment.DoesNotExist:
        pass
    
    return render(request, 'checkout/order_detail.html', {
        'order': order,
        'payment': payment,
        'status_class': order.get_status_class()
    })

@login_required
def order_history(request: HttpRequest) -> HttpResponse:
    """Show history of user's orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'checkout/order_history.html', {
        'orders': orders
    })

@login_required
@transaction.atomic
def cancel_order(request: HttpRequest, order_id: int) -> HttpResponseRedirect:
    """Cancel an order if it's eligible for cancellation"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if not order.can_be_canceled():
        messages.error(request, "This order cannot be canceled due to its current status.")
        return redirect('order_detail', order_id=order.id)
    
    # Update order status
    order.update_status('canceled')
    
    # Refund payment if it exists
    try:
        payment = Payment.objects.get(order=order)
        if payment.status == 'completed':
            payment.refund_payment()
            messages.success(request, "Your order has been canceled and payment has been refunded.")
        else:
            messages.success(request, "Your order has been canceled.")
    except Payment.DoesNotExist:
        messages.success(request, "Your order has been canceled.")
    
    # Return products to inventory
    for order_item in order.items.all():
        product = order_item.product
        product.stock += order_item.quantity
        product.save()
    
    return redirect('order_history')

# ---------- ORDER MANAGEMENT ----------
@login_required
def order_list(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'orders/order_list.html', {
        'orders': orders
    })

@login_required
@transaction.atomic
def create_order_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for creating an order from cart items"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    # Get cart items
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    
    if not cart_items.exists():
        return JsonResponse({'error': 'Your cart is empty'}, status=400)
    
    # Check stock availability
    for item in cart_items:
        if item.product.stock < item.quantity:
            return JsonResponse({
                'error': f'Not enough stock for {item.product.name}. Available: {item.product.stock}'
            }, status=400)
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        full_name=f"{request.user.first_name} {request.user.last_name}",
        email=request.user.email,
        status='pending',
        total_price=Decimal('0.00')  # Will be calculated below
    )
    
    # Create order items and calculate total
    total_price = Decimal('0.00')
    for cart_item in cart_items:
        # Create OrderItem
        order_item = OrderItem.objects.create(
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        
        # Add to order
        order.items.add(order_item)
        total_price += order_item.get_total()
        
        # Update product stock
        product = cart_item.product
        product.stock -= cart_item.quantity
        product.save()
    
    # Update order total
    order.total_price = total_price
    order.save()
    
    # Clear cart
    cart_items.delete()
    
    return JsonResponse({
        'success': True, 
        'order_id': order.id,
        'total': str(total_price)
    })
