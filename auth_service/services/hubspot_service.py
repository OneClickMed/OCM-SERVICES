"""
HubSpot CRM integration service for contact management
"""
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class HubSpotService:
    """
    Service class to handle HubSpot CRM operations
    Currently used for Beta Health signup tracking
    """

    @staticmethod
    def create_or_update_contact(email, name=None, product_name=None):
        """
        Create or update a HubSpot contact with product signup information

        Args:
            email (str): Contact email address
            name (str, optional): Contact name (first name)
            product_name (str, optional): Product name for source tracking

        Returns:
            dict: Result with success status and message
        """
        api_key = getattr(settings, 'HUBSPOT_API_KEY', None)

        if not api_key:
            logger.warning('HubSpot API key not set - skipping contact sync')
            return {
                'success': False,
                'message': 'HubSpot API key not configured',
                'skipped': True
            }

        # Only sync for Beta Health
        if product_name not in ['Beta Health', 'beta_health']:
            logger.info(f'HubSpot sync skipped for product: {product_name}')
            return {
                'success': True,
                'message': 'HubSpot sync not required for this product',
                'skipped': True
            }

        try:
            # Determine source based on product
            source = 'betahealthsignup' if product_name in ['Beta Health', 'beta_health'] else 'signup'

            # Use name or extract from email
            firstname = name or email.split('@')[0]

            # Try to create contact
            create_response = requests.post(
                'https://api.hubapi.com/crm/v3/objects/contacts',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}',
                },
                json={
                    'properties': {
                        'email': email,
                        'firstname': firstname,
                        'source': source,
                    }
                },
                timeout=10
            )

            if create_response.status_code == 200 or create_response.status_code == 201:
                logger.info(f"HubSpot contact created successfully for {email}")
                return {
                    'success': True,
                    'message': 'Contact created in HubSpot',
                    'contact_id': create_response.json().get('id')
                }

            # Contact already exists (409 Conflict)
            if create_response.status_code == 409:
                logger.info(f"HubSpot contact already exists for {email}, updating...")

                # Search for existing contact
                search_response = requests.post(
                    'https://api.hubapi.com/crm/v3/objects/contacts/search',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {api_key}',
                    },
                    json={
                        'filterGroups': [
                            {
                                'filters': [
                                    {
                                        'propertyName': 'email',
                                        'operator': 'EQ',
                                        'value': email
                                    }
                                ]
                            }
                        ],
                        'properties': ['id', 'email']
                    },
                    timeout=10
                )

                if search_response.status_code != 200:
                    logger.warning(f"Failed to search for HubSpot contact: {email}")
                    return {
                        'success': False,
                        'message': 'Failed to search for existing contact'
                    }

                search_data = search_response.json()
                results = search_data.get('results', [])

                if not results:
                    logger.warning(f"Contact exists but not found in search: {email}")
                    return {
                        'success': False,
                        'message': 'Contact exists but not found'
                    }

                contact_id = results[0].get('id')

                # Update existing contact
                update_response = requests.patch(
                    f'https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {api_key}',
                    },
                    json={
                        'properties': {
                            'source': source
                        }
                    },
                    timeout=10
                )

                if update_response.status_code in [200, 204]:
                    logger.info(f"HubSpot contact updated successfully for {email}")
                    return {
                        'success': True,
                        'message': 'Contact updated in HubSpot',
                        'contact_id': contact_id
                    }
                else:
                    logger.warning(f"Failed to update HubSpot contact: {email}")
                    return {
                        'success': False,
                        'message': f'Failed to update contact: {update_response.status_code}'
                    }

            # Other errors
            logger.warning(f"HubSpot API error: {create_response.status_code} - {create_response.text}")
            return {
                'success': False,
                'message': f'HubSpot API error: {create_response.status_code}'
            }

        except requests.exceptions.Timeout:
            logger.warning(f"HubSpot API timeout for {email}")
            return {
                'success': False,
                'message': 'HubSpot API timeout',
                'timeout': True
            }
        except requests.exceptions.RequestException as e:
            logger.warning(f"HubSpot sync failed for {email}: {str(e)}")
            return {
                'success': False,
                'message': f'Network error: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Unexpected error in HubSpot sync for {email}: {str(e)}", exc_info=True)
            return {
                'success': False,
                'message': f'Unexpected error: {str(e)}'
            }
