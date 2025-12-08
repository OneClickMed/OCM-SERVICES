from django.core.management.base import BaseCommand
from auth_service.services.firebase_service import FirebaseService
import logging

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = 'Test Firebase connection and configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--environment',
            type=str,
            choices=['test', 'prod', 'both'],
            default='both',
            help='Environment to test (test, prod, or both)'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Test email lookup for a specific user'
        )
        parser.add_argument(
            '--tenant-id',
            type=str,
            help='Tenant ID to use for email lookup'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Testing Firebase Configuration'))
        self.stdout.write('=' * 60)

        environments = ['test', 'prod'] if options['environment'] == 'both' else [options['environment']]

        for env in environments:
            self._test_environment(env, options.get('email'), options.get('tenant_id'))

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('Firebase testing complete!'))

    def _test_environment(self, environment, test_email=None, tenant_id=None):
        """Test Firebase connection for a specific environment"""
        self.stdout.write(f'\n🔥 Testing {environment.upper()} environment...')

        try:
            # Try to initialize the Firebase app
            app = FirebaseService.get_app(environment)

            if app:
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Firebase {environment} app initialized successfully'
                ))
                self.stdout.write(f'  App name: {app.name}')
                self.stdout.write(f'  Project ID: {app.project_id}')

                # If email and tenant_id provided, test user lookup
                if test_email and tenant_id:
                    self.stdout.write(f'\n  Testing user lookup for: {test_email}')
                    try:
                        user = FirebaseService.get_user_by_email(
                            test_email,
                            tenant_id,
                            environment
                        )
                        if user:
                            self.stdout.write(self.style.SUCCESS(
                                f'  ✓ User found: {user.get("email")}'
                            ))
                            self.stdout.write(f'    UID: {user.get("uid")}')
                            self.stdout.write(f'    Verified: {user.get("email_verified")}')
                        else:
                            self.stdout.write(self.style.WARNING(
                                f'  ⚠ User not found: {test_email}'
                            ))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'  ✗ Error looking up user: {e}'
                        ))

        except ValueError as e:
            self.stdout.write(self.style.ERROR(
                f'✗ Configuration error: {e}'
            ))
            self.stdout.write(f'\n  Make sure all FIREBASE_{environment.upper()}_* variables are set in .env')
            self.stdout.write(f'  Run: python manage.py setup_firebase --validate')

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'✗ Firebase initialization failed: {e}'
            ))
