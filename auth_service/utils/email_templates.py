"""
Email template utility for rendering HTML email templates with Brevo
"""
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailTemplateRenderer:
    """
    Utility class to render email templates with context variables
    """

    # Product-specific logo URLs
    PRODUCT_LOGOS = {
        'Beta Health': 'https://oneclickmed.ng/betahealth_logo.JPG',
        'beta_health': 'https://oneclickmed.ng/betahealth_logo.JPG',
        # Add more product logos here as needed
        # 'EHR': 'https://oneclickmed.ng/ehr_logo.png',
        # 'Emergency Service': 'https://oneclickmed.ng/emergency_logo.png',
    }

    # Default OneClickMed logo
    DEFAULT_LOGO = 'https://oneclickmed.ng/_next/image?url=%2Fassets%2Fimg%2Fonclickmedlogo.png&w=384&q=75'

    @staticmethod
    def get_environment_label(environment):
        """Get human-readable environment label"""
        return "Test Environment" if environment == "test" else "Production"

    @staticmethod
    def get_product_logo_url(product_name):
        """Get product-specific logo URL or default"""
        return EmailTemplateRenderer.PRODUCT_LOGOS.get(product_name, EmailTemplateRenderer.DEFAULT_LOGO)

    @staticmethod
    def get_welcome_email_sender(product_name):
        """Get special sender for welcome emails - Reagan for Beta Health, default for others"""
        if product_name in ['Beta Health', 'beta_health']:
            return {'email': 'Reagan@oneclickmed.ng', 'name': 'Reagan Rowland - OneClick-Med'}
        return None  # Use default from settings

    @staticmethod
    def render_verification_email(product_name, verification_link, environment='prod', user_name=None):
        """
        Render email verification template

        Args:
            product_name (str): Name of the product
            verification_link (str): Firebase verification link
            environment (str): 'test' or 'prod'
            user_name (str, optional): User's name

        Returns:
            dict: Contains 'subject', 'html_content', 'text_content'
        """
        context = {
            'product_name': product_name,
            'verification_link': verification_link,
            'environment': environment,
            'environment_label': EmailTemplateRenderer.get_environment_label(environment),
            'user_name': user_name,
            'product_logo_url': EmailTemplateRenderer.get_product_logo_url(product_name)
        }

        html_content = render_to_string('emails/verification_email.html', context)

        # Text content fallback
        text_content = f"""
Verify Your Email Address

Hello{' ' + user_name if user_name else ''},

Thank you for signing up with {product_name}! To complete your registration and access all features, please verify your email address.

Click here to verify: {verification_link}

Important:
- This verification link will expire in 48 hours
- If you didn't create an account with {product_name}, please ignore this email
- For security reasons, do not share this link with anyone

This email was sent from {product_name} ({EmailTemplateRenderer.get_environment_label(environment)})
"""

        subject = f"Verify Your Email - {product_name}"

        return {
            'subject': subject,
            'html_content': html_content,
            'text_content': text_content.strip()
        }

    @staticmethod
    def render_welcome_email(product_name, dashboard_link, environment='prod', user_name=None):
        """
        Render welcome email template

        Args:
            product_name (str): Name of the product
            dashboard_link (str): Link to the product dashboard
            environment (str): 'test' or 'prod'
            user_name (str, optional): User's name

        Returns:
            dict: Contains 'subject', 'html_content', 'text_content'
        """
        context = {
            'product_name': product_name,
            'dashboard_link': dashboard_link,
            'environment': environment,
            'environment_label': EmailTemplateRenderer.get_environment_label(environment),
            'user_name': user_name,
            'product_logo_url': EmailTemplateRenderer.get_product_logo_url(product_name)
        }

        html_content = render_to_string('emails/welcome_email.html', context)

        # Text content fallback
        text_content = f"""
Welcome to {product_name}!

Hello{' ' + user_name if user_name else ''},

We're thrilled to have you join {product_name}! Your account has been successfully created and verified.

You now have access to all the features and benefits of our platform. Here's what you can do next:

✓ Complete your profile - Add more information to personalize your experience
✓ Explore features - Discover all the tools available to you
✓ Get support - Our team is here to help you succeed

Get Started: {dashboard_link}

If you have any questions or need assistance, don't hesitate to reach out to our support team. We're here to help!

You're receiving this email because you created an account with {product_name}
Environment: {EmailTemplateRenderer.get_environment_label(environment)}
"""

        subject = f"Welcome to {product_name}!"

        return {
            'subject': subject,
            'html_content': html_content,
            'text_content': text_content.strip()
        }

    @staticmethod
    def render_verification_success(product_name, dashboard_link, environment='prod'):
        """
        Render verification success page HTML

        Args:
            product_name (str): Name of the product
            dashboard_link (str): Link to the product dashboard
            environment (str): 'test' or 'prod'

        Returns:
            str: HTML content for success page
        """
        context = {
            'product_name': product_name,
            'dashboard_link': dashboard_link,
            'environment': environment,
            'environment_label': EmailTemplateRenderer.get_environment_label(environment),
            'product_logo_url': EmailTemplateRenderer.get_product_logo_url(product_name)
        }

        return render_to_string('emails/verification_success.html', context)

    @staticmethod
    def render_password_reset_success(product_name, dashboard_link, environment='prod'):
        """
        Render password reset success page HTML

        Args:
            product_name (str): Name of the product
            dashboard_link (str): Link to the product dashboard
            environment (str): 'test' or 'prod'

        Returns:
            str: HTML content for success page
        """
        context = {
            'product_name': product_name,
            'dashboard_link': dashboard_link,
            'environment': environment,
            'environment_label': EmailTemplateRenderer.get_environment_label(environment),
            'product_logo_url': EmailTemplateRenderer.get_product_logo_url(product_name)
        }

        return render_to_string('emails/password_reset_success.html', context)

    @staticmethod
    def render_password_reset_email(product_name, reset_link, environment='prod', user_name=None):
        """
        Render password reset email template

        Args:
            product_name (str): Name of the product
            reset_link (str): Firebase password reset link
            environment (str): 'test' or 'prod'
            user_name (str, optional): User's name

        Returns:
            dict: Contains 'subject', 'html_content', 'text_content'
        """
        context = {
            'product_name': product_name,
            'reset_link': reset_link,
            'environment': environment,
            'environment_label': EmailTemplateRenderer.get_environment_label(environment),
            'user_name': user_name,
            'product_logo_url': EmailTemplateRenderer.get_product_logo_url(product_name)
        }

        html_content = render_to_string('emails/password_reset_email.html', context)

        # Text content fallback
        text_content = f"""
Password Reset Request

Hello{' ' + user_name if user_name else ''},

We received a request to reset the password for your {product_name} account. If you made this request, click the link below to set a new password:

{reset_link}

If you did not request a password reset, you can safely ignore this email. Your account remains secure.

Need help? Contact our support team at support@oneclickmed.ng

This email was sent from {product_name} ({EmailTemplateRenderer.get_environment_label(environment)})
"""

        subject = f"Password Reset - {product_name}"

        return {
            'subject': subject,
            'html_content': html_content,
            'text_content': text_content.strip()
        }

    @staticmethod
    def render_password_reset_form(product_name, reset_token, environment='prod', api_url=''):
        """
        Render password reset form page where user enters new password

        Args:
            product_name (str): Name of the product
            reset_token (str): Firebase password reset token
            environment (str): 'test' or 'prod'
            api_url (str): Base API URL for form submission

        Returns:
            str: HTML content for password reset form
        """
        context = {
            'product_name': product_name,
            'reset_token': reset_token,
            'environment': environment,
            'environment_label': EmailTemplateRenderer.get_environment_label(environment),
            'product_logo_url': EmailTemplateRenderer.get_product_logo_url(product_name),
            'api_url': api_url
        }

        return render_to_string('emails/password_reset_form.html', context)

    @staticmethod
    def render_password_reset_complete(product_name, dashboard_link, environment='prod'):
        """
        Render password reset completion success page

        Args:
            product_name (str): Name of the product
            dashboard_link (str): Link to the product dashboard/login
            environment (str): 'test' or 'prod'

        Returns:
            str: HTML content for password reset complete page
        """
        context = {
            'product_name': product_name,
            'dashboard_link': dashboard_link,
            'environment': environment,
            'environment_label': EmailTemplateRenderer.get_environment_label(environment),
            'product_logo_url': EmailTemplateRenderer.get_product_logo_url(product_name)
        }

        return render_to_string('emails/password_reset_complete.html', context)
