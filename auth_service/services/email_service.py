import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class BrevoEmailService:
    """
    Service class to handle email sending via Brevo (formerly Sendinblue)
    """

    def __init__(self):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        self.sender = {
            "name": settings.BREVO_SENDER_NAME,
            "email": settings.BREVO_SENDER_EMAIL
        }

    def send_email(self, to_email, subject, html_content, text_content=None,
                   template_id=None, params=None, reply_to=None, sender=None):
        """
        Send an email using Brevo API

        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            html_content (str): HTML content of the email
            text_content (str, optional): Plain text content
            template_id (int, optional): Brevo template ID
            params (dict, optional): Template parameters
            reply_to (str, optional): Reply-to email address
            sender (dict, optional): Custom sender {email, name}. Uses default if None

        Returns:
            dict: Response from Brevo API containing message_id
        """
        try:
            # Use custom sender if provided, otherwise use default
            email_sender = sender if sender else self.sender

            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": to_email}],
                sender=email_sender,
                subject=subject,
            )

            if template_id:
                send_smtp_email.template_id = template_id
                if params:
                    send_smtp_email.params = params
            else:
                send_smtp_email.html_content = html_content
                if text_content:
                    send_smtp_email.text_content = text_content

            if reply_to:
                send_smtp_email.reply_to = {"email": reply_to}

            api_response = self.api_instance.send_transac_email(send_smtp_email)

            logger.info(f"Email sent successfully to {to_email}. Message ID: {api_response.message_id}")

            return {
                'success': True,
                'message_id': api_response.message_id
            }

        except ApiException as e:
            error_msg = f"Exception when calling Brevo API: {e}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            error_msg = f"Unexpected error sending email: {e}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': str(e)
            }

    def send_generic_email(self, to_email, subject, html_content, text_content=None):
        """
        Send a generic email
        """
        return self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

    def send_password_reset_email(self, to_email, reset_link, user_name=None):
        """
        Send password reset email
        """
        subject = "Reset Your Password"
        html_content = f"""
        <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>Hello{' ' + user_name if user_name else ''},</p>
                <p>We received a request to reset your password. Click the link below to reset it:</p>
                <p><a href="{reset_link}">Reset Password</a></p>
                <p>If you didn't request this, please ignore this email.</p>
                <p>This link will expire in 24 hours.</p>
                <br>
                <p>Best regards,<br>{settings.BREVO_SENDER_NAME}</p>
            </body>
        </html>
        """
        text_content = f"""
        Password Reset Request

        Hello{' ' + user_name if user_name else ''},

        We received a request to reset your password. Copy and paste this link to reset it:
        {reset_link}

        If you didn't request this, please ignore this email.
        This link will expire in 24 hours.

        Best regards,
        {settings.BREVO_SENDER_NAME}
        """
        return self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

    def send_forgot_password_email(self, to_email, reset_link, user_name=None):
        """
        Send forgot password email (similar to password reset)
        """
        subject = "Forgot Your Password?"
        html_content = f"""
        <html>
            <body>
                <h2>Password Recovery</h2>
                <p>Hello{' ' + user_name if user_name else ''},</p>
                <p>You requested to recover your password. Click the link below to create a new password:</p>
                <p><a href="{reset_link}">Create New Password</a></p>
                <p>If you didn't request this, please ignore this email or contact support if you have concerns.</p>
                <p>This link will expire in 24 hours.</p>
                <br>
                <p>Best regards,<br>{settings.BREVO_SENDER_NAME}</p>
            </body>
        </html>
        """
        text_content = f"""
        Password Recovery

        Hello{' ' + user_name if user_name else ''},

        You requested to recover your password. Copy and paste this link to create a new password:
        {reset_link}

        If you didn't request this, please ignore this email or contact support if you have concerns.
        This link will expire in 24 hours.

        Best regards,
        {settings.BREVO_SENDER_NAME}
        """
        return self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

    def send_verification_email(self, to_email, verification_link, user_name=None):
        """
        Send email verification email
        """
        subject = "Verify Your Email Address"
        html_content = f"""
        <html>
            <body>
                <h2>Email Verification</h2>
                <p>Hello{' ' + user_name if user_name else ''},</p>
                <p>Thank you for registering! Please verify your email address by clicking the link below:</p>
                <p><a href="{verification_link}">Verify Email Address</a></p>
                <p>If you didn't create an account, please ignore this email.</p>
                <p>This link will expire in 48 hours.</p>
                <br>
                <p>Best regards,<br>{settings.BREVO_SENDER_NAME}</p>
            </body>
        </html>
        """
        text_content = f"""
        Email Verification

        Hello{' ' + user_name if user_name else ''},

        Thank you for registering! Please verify your email address by copying and pasting this link:
        {verification_link}

        If you didn't create an account, please ignore this email.
        This link will expire in 48 hours.

        Best regards,
        {settings.BREVO_SENDER_NAME}
        """
        return self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )
