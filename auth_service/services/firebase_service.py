import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
import logging
import json
import requests

logger = logging.getLogger(__name__)


class FirebaseService:
    """
    Service class to handle Firebase authentication operations.
    Uses Firebase credentials from environment variables (JSON strings).
    """
    _test_app = None
    _prod_app = None

    @classmethod
    def _initialize_app(cls, environment='test'):
        """
        Initialize Firebase app for the specified environment using credentials from env vars
        """
        if environment == 'prod':
            if cls._prod_app is None:
                cred_dict = settings.FIREBASE_PROD_CONFIG

                # Validate required fields
                required_fields = ['project_id', 'private_key', 'client_email']
                missing_fields = [f for f in required_fields if not cred_dict.get(f)]

                if missing_fields:
                    logger.error(f"Missing Firebase production credentials: {', '.join(missing_fields)}")
                    raise ValueError(f"Missing Firebase production config fields: {', '.join(missing_fields)}")

                try:
                    cred = credentials.Certificate(cred_dict)
                    cls._prod_app = firebase_admin.initialize_app(
                        cred,
                        name='prod',
                        options={'projectId': cred_dict.get('project_id')}
                    )
                    logger.info(f"Firebase production app initialized - Project: {cred_dict.get('project_id')}")
                except Exception as e:
                    logger.error(f"Error initializing Firebase production app: {e}")
                    raise ValueError(f"Failed to initialize Firebase production: {e}")
            return cls._prod_app
        else:
            if cls._test_app is None:
                cred_dict = settings.FIREBASE_TEST_CONFIG

                # Validate required fields
                required_fields = ['project_id', 'private_key', 'client_email']
                missing_fields = [f for f in required_fields if not cred_dict.get(f)]

                if missing_fields:
                    logger.error(f"Missing Firebase test credentials: {', '.join(missing_fields)}")
                    raise ValueError(f"Missing Firebase test config fields: {', '.join(missing_fields)}")

                try:
                    cred = credentials.Certificate(cred_dict)
                    cls._test_app = firebase_admin.initialize_app(
                        cred,
                        name='test',
                        options={'projectId': cred_dict.get('project_id')}
                    )
                    logger.info(f"Firebase test app initialized - Project: {cred_dict.get('project_id')}")
                except Exception as e:
                    logger.error(f"Error initializing Firebase test app: {e}")
                    raise ValueError(f"Failed to initialize Firebase test: {e}")
            return cls._test_app

    @classmethod
    def get_app(cls, environment='test'):
        """
        Get Firebase app instance for the specified environment
        """
        try:
            return cls._initialize_app(environment)
        except Exception as e:
            logger.error(f"Error initializing Firebase app for {environment}: {e}")
            raise

    @classmethod
    def _get_access_token(cls, environment='test'):
        """
        Get OAuth2 access token for Firebase REST API calls

        Args:
            environment (str): 'test' or 'prod'

        Returns:
            str: Access token
        """
        try:
            app = cls.get_app(environment)
            # Get credentials from the app and fetch access token
            access_token = app.credential.get_access_token().access_token
            return access_token
        except Exception as e:
            logger.error(f"Error getting access token: {e}")
            raise

    @classmethod
    def generate_password_reset_link(cls, email, tenant_id, environment='test'):
        """
        Generate a password reset link for a user using tenant-scoped Firebase Identity Platform API

        Args:
            email (str): User's email address
            tenant_id (str): Firebase tenant ID
            environment (str): 'test' or 'prod'

        Returns:
            str: Password reset link
        """
        try:
            # Get access token (this also initializes the app if needed)
            access_token = cls._get_access_token(environment)

            # Use Firebase Identity Platform REST API for tenant-scoped operations
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            params = {}
            if tenant_id:
                params['tenantId'] = tenant_id

            payload = {
                'requestType': 'PASSWORD_RESET',
                'email': email,
                'returnOobLink': True  # Get the link in the response instead of sending email
            }

            response = requests.post(url, headers=headers, params=params, json=payload)

            if response.status_code == 200:
                result = response.json()
                link = result.get('oobLink')
                logger.info(f"Password reset link generated for {email} in {environment} environment (tenant_id: {tenant_id})")
                return link
            else:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Unknown error')

                # Handle specific error cases
                if 'EMAIL_NOT_FOUND' in error_message or 'USER_NOT_FOUND' in error_message:
                    logger.warning(f"User not found: {email} in tenant {tenant_id}")
                    raise ValueError(f"User with email {email} not found")
                else:
                    logger.error(f"Firebase API error: {error_message}")
                    raise Exception(f"Firebase API error: {error_message}")

        except ValueError:
            # Re-raise ValueError for user not found
            raise
        except Exception as e:
            logger.error(f"Error generating password reset link: {e}")
            raise

    @classmethod
    def generate_email_verification_link(cls, email, tenant_id, environment='test'):
        """
        Generate an email verification link for a user using tenant-scoped Firebase Identity Platform API

        Args:
            email (str): User's email address
            tenant_id (str): Firebase tenant ID
            environment (str): 'test' or 'prod'

        Returns:
            str: Email verification link
        """
        try:
            # Get access token (this also initializes the app if needed)
            access_token = cls._get_access_token(environment)

            # Use Firebase Identity Platform REST API for tenant-scoped operations
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            params = {}
            if tenant_id:
                params['tenantId'] = tenant_id

            payload = {
                'requestType': 'VERIFY_EMAIL',
                'email': email,
                'returnOobLink': True  # Get the link in the response instead of sending email
            }

            response = requests.post(url, headers=headers, params=params, json=payload)

            if response.status_code == 200:
                result = response.json()
                link = result.get('oobLink')
                logger.info(f"Email verification link generated for {email} in {environment} environment (tenant_id: {tenant_id})")
                return link
            else:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Unknown error')

                # Handle specific error cases
                if 'EMAIL_NOT_FOUND' in error_message or 'USER_NOT_FOUND' in error_message:
                    logger.warning(f"User not found: {email} in tenant {tenant_id}")
                    raise ValueError(f"User with email {email} not found")
                else:
                    logger.error(f"Firebase API error: {error_message}")
                    raise Exception(f"Firebase API error: {error_message}")

        except ValueError:
            # Re-raise ValueError for user not found
            raise
        except Exception as e:
            logger.error(f"Error generating email verification link: {e}")
            raise

    @classmethod
    def get_user_by_email(cls, email, tenant_id, environment='test'):
        """
        Get user information by email

        Args:
            email (str): User's email address
            tenant_id (str): Firebase tenant ID
            environment (str): 'test' or 'prod'

        Returns:
            dict: User information
        """
        try:
            app = cls.get_app(environment)

            user = auth.get_user_by_email(
                email,
                app=app,
                tenant_id=tenant_id
            )

            return {
                'uid': user.uid,
                'email': user.email,
                'email_verified': user.email_verified,
                'display_name': user.display_name,
                'disabled': user.disabled,
            }

        except auth.UserNotFoundError:
            logger.warning(f"User not found: {email}")
            return None
        except Exception as e:
            logger.error(f"Error fetching user: {e}")
            raise

    @classmethod
    def confirm_password_reset(cls, token, new_password, environment='test'):
        """
        Confirm password reset with Firebase

        Note: Firebase Admin SDK doesn't have a direct method to confirm password reset.
        The password reset is handled client-side by Firebase Auth.
        This method is a placeholder that returns success assuming the token is valid.

        In production, the actual password reset happens when the user clicks the link
        from their email and Firebase handles it automatically.

        Args:
            token (str): Password reset token from email link
            new_password (str): New password
            environment (str): 'test' or 'prod'

        Returns:
            dict: Result with success status
        """
        try:
            # Firebase Admin SDK doesn't support confirming password reset server-side
            # The password reset must be completed using Firebase Client SDK
            # This endpoint should ideally redirect to a page that uses Firebase Client SDK

            logger.info(f"Password reset confirmation attempted in {environment} environment")

            return {
                'success': True,
                'message': 'Password reset handled by Firebase client-side'
            }

        except Exception as e:
            logger.error(f"Error in password reset confirmation: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    @classmethod
    def verify_id_token(cls, id_token, tenant_id, environment='test'):
        """
        Verify a Firebase ID token

        Args:
            id_token (str): Firebase ID token
            tenant_id (str): Firebase tenant ID
            environment (str): 'test' or 'prod'

        Returns:
            dict: Decoded token
        """
        try:
            app = cls.get_app(environment)

            decoded_token = auth.verify_id_token(
                id_token,
                app=app,
                check_revoked=True,
                tenant_id=tenant_id
            )

            return decoded_token

        except auth.InvalidIdTokenError:
            logger.warning("Invalid Firebase ID token")
            raise ValueError("Invalid token")
        except auth.ExpiredIdTokenError:
            logger.warning("Expired Firebase ID token")
            raise ValueError("Token expired")
        except auth.RevokedIdTokenError:
            logger.warning("Revoked Firebase ID token")
            raise ValueError("Token revoked")
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            raise
