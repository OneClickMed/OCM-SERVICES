from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import logging

from .serializers import (
    GenericEmailSerializer,
    PasswordResetSerializer,
    ForgotPasswordSerializer,
    EmailVerificationSerializer,
    WelcomeEmailSerializer,
    VerifyEmailConfirmationSerializer,
    EmailResponseSerializer
)
from .services.email_service import BrevoEmailService
from .services.firebase_service import FirebaseService
from .models import Product
from .utils.email_templates import EmailTemplateRenderer
from django.http import HttpResponse

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='60/m', method='POST'), name='post')
class GenericEmailView(APIView):
    """
    API endpoint to send generic emails
    POST /api/email/generic/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GenericEmailSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid request data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Get product from authenticated user
        try:
            product = request.user.product
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User is not associated with a product'
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            # Send email via Brevo
            email_service = BrevoEmailService()
            result = email_service.send_generic_email(
                to_email=data['to_email'],
                subject=data['subject'],
                html_content=data['html_content'],
                text_content=data.get('text_content')
            )

            if result['success']:
                logger.info(f"Generic email sent successfully to {data['to_email']} by {product.display_name}")
                return Response({
                    'success': True,
                    'message': 'Email sent successfully',
                    'data': {
                        'message_id': result.get('message_id')
                    }
                }, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Failed to send generic email to {data['to_email']}: {result.get('error')}")
                return Response({
                    'success': False,
                    'message': 'Failed to send email',
                    'error': result.get('error')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Error sending generic email: {e}", exc_info=True)
            return Response({
                'success': False,
                'message': 'An error occurred while sending email',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='30/m', method='POST'), name='post')
class PasswordResetView(APIView):
    """
    API endpoint to send password reset emails
    POST /api/email/password-reset/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid request data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Get product from authenticated user
        try:
            product = request.user.product
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User is not associated with a product'
            }, status=status.HTTP_403_FORBIDDEN)

        environment = data['environment']
        environment_label = "test environment" if environment == "test" else "production environment"

        try:
            # Get Firebase tenant ID
            tenant_id = product.get_tenant_id(environment)

            # Generate password reset link from Firebase
            reset_link = FirebaseService.generate_password_reset_link(
                email=data['email'],
                tenant_id=tenant_id,
                environment=environment
            )

            # Render email template
            email_content = EmailTemplateRenderer.render_password_reset_email(
                product_name=product.display_name,
                reset_link=reset_link,
                environment=environment,
                user_name=data.get('user_name')
            )

            # Send email via Brevo
            email_service = BrevoEmailService()
            result = email_service.send_email(
                to_email=data['email'],
                subject=email_content['subject'],
                html_content=email_content['html_content'],
                text_content=email_content['text_content']
            )

            if result['success']:
                logger.info(f"Password reset email sent successfully to {data['email']} by {product.display_name}")
                return Response({
                    'success': True,
                    'message': f'Password reset email sent successfully to {environment_label}',
                    'data': {
                        'message_id': result.get('message_id'),
                        'environment': environment
                    }
                }, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Failed to send password reset email: {result.get('error')}")
                return Response({
                    'success': False,
                    'message': f'Failed to send password reset email in {environment_label}',
                    'error': result.get('error')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValueError as e:
            logger.warning(f"User not found for password reset: {e}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error sending password reset email: {e}", exc_info=True)
            return Response({
                'success': False,
                'message': f'An error occurred while sending password reset email in {environment_label}',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='30/m', method='POST'), name='post')
class ForgotPasswordView(APIView):
    """
    API endpoint to send forgot password emails (same as password reset)
    POST /api/email/forgot-password/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid request data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Get product from authenticated user
        try:
            product = request.user.product
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User is not associated with a product'
            }, status=status.HTTP_403_FORBIDDEN)

        environment = data['environment']
        environment_label = "test environment" if environment == "test" else "production environment"

        try:
            # Get Firebase tenant ID
            tenant_id = product.get_tenant_id(environment)

            # Generate password reset link from Firebase
            reset_link = FirebaseService.generate_password_reset_link(
                email=data['email'],
                tenant_id=tenant_id,
                environment=environment
            )

            # Render email template
            email_content = EmailTemplateRenderer.render_password_reset_email(
                product_name=product.display_name,
                reset_link=reset_link,
                environment=environment,
                user_name=data.get('user_name')
            )

            # Send email via Brevo
            email_service = BrevoEmailService()
            result = email_service.send_email(
                to_email=data['email'],
                subject=email_content['subject'],
                html_content=email_content['html_content'],
                text_content=email_content['text_content']
            )

            if result['success']:
                logger.info(f"Forgot password email sent successfully to {data['email']} by {product.display_name}")
                return Response({
                    'success': True,
                    'message': f'Forgot password email sent successfully to {environment_label}',
                    'data': {
                        'message_id': result.get('message_id'),
                        'environment': environment
                    }
                }, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Failed to send forgot password email: {result.get('error')}")
                return Response({
                    'success': False,
                    'message': f'Failed to send forgot password email in {environment_label}',
                    'error': result.get('error')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValueError as e:
            logger.warning(f"User not found for forgot password: {e}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error sending forgot password email: {e}", exc_info=True)
            return Response({
                'success': False,
                'message': f'An error occurred while sending forgot password email in {environment_label}',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='30/m', method='POST'), name='post')
class EmailVerificationView(APIView):
    """
    API endpoint to send email verification with product branding
    POST /api/email/verification/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid request data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Get product from authenticated user
        try:
            product = request.user.product
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User is not associated with a product'
            }, status=status.HTTP_403_FORBIDDEN)

        environment = data['environment']
        environment_label = "test environment" if environment == "test" else "production environment"

        try:
            # Get Firebase tenant ID
            tenant_id = product.get_tenant_id(environment)

            # Generate email verification link from Firebase
            verification_link = FirebaseService.generate_email_verification_link(
                email=data['email'],
                tenant_id=tenant_id,
                environment=environment
            )

            # Render email template with product branding
            email_content = EmailTemplateRenderer.render_verification_email(
                product_name=product.display_name,
                verification_link=verification_link,
                environment=environment,
                user_name=data.get('user_name')
            )

            # Send email via Brevo
            email_service = BrevoEmailService()
            result = email_service.send_email(
                to_email=data['email'],
                subject=email_content['subject'],
                html_content=email_content['html_content'],
                text_content=email_content['text_content']
            )

            if result['success']:
                logger.info(f"Verification email sent successfully to {data['email']} by {product.display_name}")
                return Response({
                    'success': True,
                    'message': f'Verification email sent successfully to {environment_label}',
                    'data': {
                        'message_id': result.get('message_id'),
                        'product_name': product.display_name,
                        'environment': environment
                    }
                }, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Failed to send verification email: {result.get('error')}")
                return Response({
                    'success': False,
                    'message': f'Failed to send verification email in {environment_label}',
                    'error': result.get('error')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValueError as e:
            logger.warning(f"User not found for email verification: {e}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error sending verification email: {e}", exc_info=True)
            return Response({
                'success': False,
                'message': f'An error occurred while sending verification email in {environment_label}',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class VerifyEmailConfirmationView(APIView):
    """
    API endpoint to confirm email verification and show success page
    GET /api/email/verify-confirmation/
    This endpoint is typically called when user clicks the verification link in their email
    """
    permission_classes = []

    def get(self, request):
        # Get token and environment from query parameters
        token = request.GET.get('token', '')
        environment = request.GET.get('environment', 'prod')
        product_name = request.GET.get('product', 'Our Service')

        if not token:
            return HttpResponse(
                '<h1>Invalid Verification Link</h1><p>The verification link is missing required parameters.</p>',
                status=400
            )

        try:
            # Note: Firebase automatically verifies the email when user clicks the link
            # This endpoint is just to show a branded success page

            # Get dashboard link from settings or use default
            # You can customize this per product in the future
            dashboard_link = f"https://app.example.com/dashboard?environment={environment}"

            # Render success page
            success_html = EmailTemplateRenderer.render_verification_success(
                product_name=product_name,
                dashboard_link=dashboard_link,
                environment=environment
            )

            return HttpResponse(success_html)

        except Exception as e:
            logger.error(f"Error in verification confirmation: {e}", exc_info=True)
            return HttpResponse(
                '<h1>Verification Error</h1><p>An error occurred while processing your verification.</p>',
                status=500
            )


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='30/m', method='POST'), name='post')
class WelcomeEmailView(APIView):
    """
    API endpoint to send welcome email with product branding
    POST /api/email/welcome/
    Automatically adds user to HubSpot CRM for Beta Health
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WelcomeEmailSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid request data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Get product from authenticated user
        try:
            product = request.user.product
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User is not associated with a product'
            }, status=status.HTTP_403_FORBIDDEN)

        environment = data['environment']
        environment_label = "test environment" if environment == "test" else "production environment"

        try:
            # Get dashboard link based on environment
            # You can customize this per product from settings
            dashboard_link = f"https://app.example.com/dashboard?environment={environment}"

            # Render welcome email template with product branding
            email_content = EmailTemplateRenderer.render_welcome_email(
                product_name=product.display_name,
                dashboard_link=dashboard_link,
                environment=environment,
                user_name=data.get('user_name')
            )

            # Get custom sender for Beta Health welcome emails
            custom_sender = EmailTemplateRenderer.get_welcome_email_sender(product.display_name)

            # Send email via Brevo
            email_service = BrevoEmailService()
            result = email_service.send_email(
                to_email=data['email'],
                subject=email_content['subject'],
                html_content=email_content['html_content'],
                text_content=email_content['text_content'],
                sender=custom_sender
            )

            if result['success']:
                logger.info(f"Welcome email sent successfully to {data['email']} by {product.display_name}")

                # Add user to HubSpot CRM (Beta Health only)
                from .services.hubspot_service import HubSpotService
                hubspot_result = HubSpotService.create_or_update_contact(
                    email=data['email'],
                    name=data.get('user_name'),
                    product_name=product.display_name
                )

                logger.info(f"HubSpot sync result: {hubspot_result}")

                return Response({
                    'success': True,
                    'message': f'Welcome email sent successfully to {environment_label}',
                    'data': {
                        'message_id': result.get('message_id'),
                        'product_name': product.display_name,
                        'environment': environment,
                        'hubspot_synced': hubspot_result.get('success', False)
                    }
                }, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Failed to send welcome email: {result.get('error')}")
                return Response({
                    'success': False,
                    'message': f'Failed to send welcome email in {environment_label}',
                    'error': result.get('error')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Error sending welcome email: {e}", exc_info=True)
            return Response({
                'success': False,
                'message': f'An error occurred while sending welcome email in {environment_label}',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetFormView(APIView):
    """
    API endpoint to display password reset form
    GET /api/password/reset-form/
    """
    permission_classes = []

    def get(self, request):
        # Get parameters from query string
        token = request.GET.get('token', '')
        environment = request.GET.get('environment', 'prod')
        product_name = request.GET.get('product', 'OneClickMed')

        if not token:
            return HttpResponse(
                '<h1>Invalid Reset Link</h1><p>The password reset link is missing required parameters.</p>',
                status=400
            )

        try:
            # Get API URL from settings
            from django.conf import settings
            api_url = getattr(settings, 'BACKEND_URL', 'https://auth.oneclickmed.ng')

            # Render password reset form
            form_html = EmailTemplateRenderer.render_password_reset_form(
                product_name=product_name,
                reset_token=token,
                environment=environment,
                api_url=api_url
            )

            return HttpResponse(form_html)

        except Exception as e:
            logger.error(f"Error displaying password reset form: {e}", exc_info=True)
            return HttpResponse(
                '<h1>Error</h1><p>An error occurred while loading the password reset form.</p>',
                status=500
            )


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='10/h', method='POST'), name='post')
class PasswordResetConfirmView(APIView):
    """
    API endpoint to handle password reset form submission
    POST /api/password/reset-confirm/
    """
    permission_classes = []

    def post(self, request):
        try:
            token = request.data.get('token')
            new_password = request.data.get('new_password')
            product_name = request.data.get('product', 'OneClickMed')
            environment = request.data.get('environment', 'prod')

            if not token or not new_password:
                return Response({
                    'success': False,
                    'message': 'Token and new password are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate password strength
            if len(new_password) < 8:
                return Response({
                    'success': False,
                    'message': 'Password must be at least 8 characters long'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Confirm password reset with Firebase
            firebase_result = FirebaseService.confirm_password_reset(
                token=token,
                new_password=new_password,
                environment=environment
            )

            if firebase_result['success']:
                logger.info(f"Password reset successful for {product_name}")

                # Get success page URL
                from django.conf import settings
                api_url = getattr(settings, 'BACKEND_URL', 'https://auth.oneclickmed.ng')
                success_url = f"{api_url}/api/password/reset-complete/?product={product_name}&environment={environment}"

                return Response({
                    'success': True,
                    'message': 'Password reset successful',
                    'redirect_url': success_url
                }, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Password reset failed: {firebase_result.get('error')}")
                return Response({
                    'success': False,
                    'message': firebase_result.get('error', 'Password reset failed')
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error confirming password reset: {e}", exc_info=True)
            return Response({
                'success': False,
                'message': 'An error occurred while resetting password'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetCompleteView(APIView):
    """
    API endpoint to display password reset completion success page
    GET /api/password/reset-complete/
    """
    permission_classes = []

    def get(self, request):
        # Get parameters from query string
        product_name = request.GET.get('product', 'OneClickMed')
        environment = request.GET.get('environment', 'prod')

        try:
            # Get dashboard link - customize per product
            dashboard_links = {
                'Beta Health': 'https://betahealth.oneclickmed.ng',
                'EHR': 'https://ehr.oneclickmed.ng',
                'Emergency Service': 'https://emergency.oneclickmed.ng',
            }
            dashboard_link = dashboard_links.get(product_name, 'https://oneclickmed.ng')

            # Render password reset complete page
            complete_html = EmailTemplateRenderer.render_password_reset_complete(
                product_name=product_name,
                dashboard_link=dashboard_link,
                environment=environment
            )

            return HttpResponse(complete_html)

        except Exception as e:
            logger.error(f"Error displaying password reset complete page: {e}", exc_info=True)
            return HttpResponse(
                '<h1>Success</h1><p>Your password has been reset successfully.</p>',
                status=200
            )


class HealthCheckView(APIView):
    """
    API endpoint for health check
    GET /api/health/
    """
    permission_classes = []

    def get(self, request):
        return Response({
            'success': True,
            'message': 'Service is running',
            'status': 'healthy'
        }, status=status.HTTP_200_OK)


class PingDatabaseView(APIView):
    """
    API endpoint to ping database and keep it active
    GET /api/ping/
    This endpoint makes a simple database query to prevent Supabase from going inactive
    """
    permission_classes = []

    def get(self, request):
        try:
            from django.db import connection

            # Execute a simple query to wake up the database
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

            return Response({
                'success': True,
                'message': 'Database is active',
                'status': 'connected'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Database ping failed: {e}")
            return Response({
                'success': False,
                'message': 'Database connection failed',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
