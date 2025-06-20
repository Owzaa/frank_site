from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from typing import Dict, List, Optional, Union, Any, Tuple, ClassVar, cast

# STORE_MODEL
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.IntegerField()
    available = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/products/product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_total(self):
        return self.price * self.quantity
    
    @property
    def total_price(self):
        return self.get_total()

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(OrderItem)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20,null=True)
    shipping_address = models.CharField(max_length=250,null=True)
    address = models.CharField(max_length=250, blank=True, null=True)  # Keeping for backward compatibility
    city = models.CharField(max_length=100, blank=True, null=True)  # Keeping for backward compatibility
    postal_code = models.CharField(max_length=20, blank=True, null=True)  # Keeping for backward compatibility
    country = models.CharField(max_length=100,blank=True, null=True)  # Keeping for backward compatibility  
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processing_date = models.DateTimeField(blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    cancelled_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
    def get_total_cost(self):
        return sum(item.get_total() for item in self.items.all()) + self.shipping_cost
    
    def update_status(self, status):
        """Update order status and set the appropriate timestamp"""
        self.status = status
        
        if status == 'processing':
            self.processing_date = timezone.now()
        elif status == 'shipped':
            self.shipped_date = timezone.now()
        elif status == 'delivered':
            self.delivered_date = timezone.now()
        elif status == 'cancelled':
            self.cancelled_date = timezone.now()
        
        self.save()
    
    def get_status_display_class(self) -> str:
        """Return Bootstrap class for status badge"""
        status_classes: Dict[str, str] = {
            'pending': 'bg-warning text-dark',
            'processing': 'bg-info',
            'shipped': 'bg-primary',
            'delivered': 'bg-success',
            'cancelled': 'bg-danger',
            'completed': 'bg-success'
        }
        return status_classes.get(cast(str, self.status), 'bg-secondary')
        
    def can_cancel(self) -> bool:
        """Check if order can be cancelled"""
        return self.status in ['pending', 'processing']

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES: ClassVar[Tuple[Tuple[str, str], ...]] = (
        ('paypal', 'PayPal'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
    )
    STATUS_CHOICES: ClassVar[Tuple[Tuple[str, str], ...]] = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at: Optional[models.DateTimeField] = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"
    
    def complete_payment(self, transaction_id: Optional[str] = None) -> bool:
        """Mark payment as completed and update order status"""
        self.status = 'completed'
        if transaction_id:
            self.transaction_id = transaction_id
        self.completed_at = timezone.now()
        self.save()
        
        # Update order status
        self.order.update_status('processing')
        return True
    
    def fail_payment(self, reason=None):
        """Mark payment as failed"""
        self.status = 'failed'
        self.save()
        return False
    
    def refund_payment(self):
        """Process a refund"""
        if self.status != 'completed':
            return False
        
        self.status = 'refunded'
        self.save()
        
        # Update order status if it's not already cancelled
        if self.order.status != 'cancelled':
            self.order.update_status('cancelled')
        return True
    
    def get_status_display_class(self) -> str:
        """Return Bootstrap class for status badge"""
        status_classes: Dict[str, str] = {
            'pending': 'bg-warning text-dark',
            'completed': 'bg-success',
            'failed': 'bg-danger',
            'refunded': 'bg-info'
        }
        return status_classes.get(cast(str, self.status), 'bg-secondary')

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_cards')
    card_number = models.CharField(max_length=16)  # Store securely in production
    card_holder = models.CharField(max_length=100)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=4)
    cvv = models.CharField(max_length=4)  # Don't store in production
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Card ending in {self.masked_number} for {self.user.username}"
    
    @property
    def masked_number(self):
        """Return masked card number for display"""
        if len(self.card_number) < 4:
            return "****"
        return "*" * (len(self.card_number) - 4) + self.card_number[-4:]
    
    @property
    def expiry_date_formatted(self):
        """Return formatted expiry date"""
        return f"{self.expiry_month}/{self.expiry_year}"
    
    def is_expired(self):
        """Check if card is expired"""
        current_year = timezone.now().year
        current_month = timezone.now().month
        
        try:
            year = int(self.expiry_year)
            month = int(self.expiry_month)
            
            if year < current_year:
                return True
            if year == current_year and month < current_month:
                return True
            return False
        except ValueError:
            # If expiry date is invalid, consider it expired
            return True
    
    def save(self, *args, **kwargs):
        # In production, encrypt card details before saving
        # This is just a placeholder implementation
        super().save(*args, **kwargs)
        
        # If this card is set as default, unset other default cards
        if self.is_default:
            CreditCard.objects.filter(user=self.user).exclude(id=self.id).update(is_default=False)


class CartItem(models.Model):
    """Model for storing cart items in session"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)  # For anonymous users
    
    def __str__(self):
        if self.user:
            return f"{self.quantity} x {self.product.name} in {self.user.username}'s cart"
        return f"{self.quantity} x {self.product.name} in session {self.session_id}"
    
    @property
    def price(self):
        return self.product.price
    
    @property
    def total(self):
        return self.price * self.quantity
