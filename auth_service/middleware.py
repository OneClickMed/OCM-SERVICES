"""
Middleware for auth_service
"""
from django.utils.deprecation import MiddlewareMixin
from .models import Product
import logging

logger = logging.getLogger(__name__)


class ProductAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to attach the product to the request object based on the authenticated user.
    This allows views to easily access request.product
    """

    def process_request(self, request):
        """
        Attach product to request if user is authenticated
        """
        request.product = None

        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                # Try to get the product associated with the authenticated user
                request.product = Product.objects.get(user=request.user)
                logger.debug(f"Product {request.product.name} attached to request for user {request.user.username}")
            except Product.DoesNotExist:
                logger.warning(f"No product found for authenticated user {request.user.username}")
            except Exception as e:
                logger.error(f"Error attaching product to request: {e}")

        return None
