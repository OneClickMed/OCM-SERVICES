from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Product(models.Model):
    """
    Model to store product configurations.
    Each product is linked to a Django User with a DRF Token.
    """
    PRODUCT_CHOICES = [
        ('beta_health', 'Beta Health'),
        ('ehr', 'EHR'),
        ('emergency_service', 'Emergency Service'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='product')
    name = models.CharField(max_length=100, unique=True, choices=PRODUCT_CHOICES)
    display_name = models.CharField(max_length=200)
    test_tenant_id = models.CharField(max_length=255)
    prod_tenant_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.display_name

    def get_tenant_id(self, environment='test'):
        """
        Get Firebase tenant ID based on environment
        """
        return self.prod_tenant_id if environment == 'prod' else self.test_tenant_id

    @property
    def token(self):
        """
        Get the DRF token for this product's user
        """
        try:
            return Token.objects.get(user=self.user)
        except Token.DoesNotExist:
            return Token.objects.create(user=self.user)
