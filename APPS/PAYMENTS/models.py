from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from typing import Dict, List, Optional, Union, Any, Tuple, ClassVar, cast
from decimal import Decimal

class PaymentGateway(models.Model):
    """Model for payment gateways supported by the system"""
    GATEWAY_TYPES = [
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
    ]
    
    name = models.CharField(max_length=100)
    gateway_type = models.CharField(max_length=50, choices=GATEWAY_TYPES)
    is_active = models.BooleanField(default=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    secret_key = models.CharField(max_length=255, blank=True, null=True)
    config = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.get_gateway_type_display()})"

class PaymentMode(models.Model):
    """Enhanced payment model with better tracking and integration"""
    STATUS_CHOICES: ClassVar[List[Tuple[str, str]]] = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    order_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='ZAR')
    gateway = models.ForeignKey(PaymentGateway, on_delete=models.PROTECT, related_name='payments', null=True, blank=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    transaction_data = models.JSONField(default=dict, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    refunded_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"Payment {self.transaction_id} by {self.user.username}"
    
    def complete_payment(self, transaction_id: Optional[str] = None) -> bool:
        """Mark payment as completed"""
        self.status = 'completed'
        if transaction_id:
            self.transaction_id = transaction_id
        self.completed_at = timezone.now()
        self.save()
        return True
    
    def fail_payment(self, error_message: Optional[str] = None) -> bool:
        """Mark payment as failed"""
        self.status = 'failed'
        if error_message:
            self.error_message = error_message
        self.save()
        return False
    
    def refund_payment(self, amount: Optional[Decimal] = None) -> bool:
        """Process a refund"""
        if self.status != 'completed':
            return False
        
        self.status = 'refunded'
        self.refunded_at = timezone.now()
        self.save()
        return True
    
    def get_status_display_class(self) -> str:
        """Return Bootstrap class for status badge"""
        status_classes: Dict[str, str] = {
            'pending': 'bg-warning text-dark',
            'processing': 'bg-info',
            'completed': 'bg-success',
            'failed': 'bg-danger',
            'refunded': 'bg-secondary',
            'cancelled': 'bg-dark'
        }
        return status_classes.get(cast(str, self.status), 'bg-secondary')

class PaymentMethod(models.Model):
    """Model for storing user's payment methods"""
    METHOD_TYPES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal Account'),
        ('bank_account', 'Bank Account'),
        ('crypto_wallet', 'Crypto Wallet'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    method_type = models.CharField(max_length=50, choices=METHOD_TYPES)
    name = models.CharField(max_length=100)  # User-friendly name for this payment method
    is_default = models.BooleanField(default=False)
    details = models.JSONField(default=dict)  # Encrypted in production
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.get_method_type_display()}) - {self.user.username}"
    
    def save(self, *args, **kwargs):
        # If this method is set as default, unset other default methods
        if self.is_default:
            PaymentMethod.objects.filter(user=self.user).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)
    
    @property
    def masked_details(self) -> Dict[str, Any]:
        """Return masked version of payment details for display"""
        masked = {}
        if self.method_type == 'credit_card' and 'card_number' in self.details:
            card_number = self.details.get('card_number', '')
            if len(card_number) > 4:
                masked['card_number'] = '*' * (len(card_number) - 4) + card_number[-4:]
            else:
                masked['card_number'] = '****'
            
            masked['expiry'] = self.details.get('expiry_month', '') + '/' + self.details.get('expiry_year', '')
            masked['card_holder'] = self.details.get('card_holder', '')
        
        return masked
