from django.core.management.base import BaseCommand
import json
import os


class Command(BaseCommand):
    help = 'Helper command to convert Firebase JSON files to environment variable format'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-file',
            type=str,
            help='Path to Firebase test credentials JSON file'
        )
        parser.add_argument(
            '--prod-file',
            type=str,
            help='Path to Firebase production credentials JSON file'
        )
        parser.add_argument(
            '--validate',
            action='store_true',
            help='Validate current environment variables'
        )

    def handle(self, *args, **options):
        if options['validate']:
            self.validate_credentials()
        else:
            self.convert_files(options['test_file'], options['prod_file'])

    def validate_credentials(self):
        """Validate Firebase credentials in environment"""
        self.stdout.write(self.style.WARNING('Validating Firebase credentials...'))

        from django.conf import settings

        # Check test credentials
        test_config = settings.FIREBASE_TEST_CONFIG
        required_fields = ['project_id', 'private_key', 'client_email']

        test_missing = [f for f in required_fields if not test_config.get(f)]
        if not test_missing:
            self.stdout.write(self.style.SUCCESS(
                f'✓ Test credentials valid - Project: {test_config.get("project_id")}'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f'⚠ Test credentials incomplete - Missing: {", ".join(test_missing)}'
            ))

        # Check prod credentials
        prod_config = settings.FIREBASE_PROD_CONFIG
        prod_missing = [f for f in required_fields if not prod_config.get(f)]

        if not prod_missing:
            self.stdout.write(self.style.SUCCESS(
                f'✓ Prod credentials valid - Project: {prod_config.get("project_id")}'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f'⚠ Prod credentials incomplete - Missing: {", ".join(prod_missing)}'
            ))

    def convert_files(self, test_file, prod_file):
        """Convert Firebase JSON files to env var format"""
        self.stdout.write(self.style.WARNING('Firebase Credentials Setup Helper'))
        self.stdout.write('=' * 60)

        if not test_file and not prod_file:
            self.stdout.write(self.style.ERROR(
                '\nError: Please provide at least one credential file.\n'
            ))
            self.stdout.write('Usage examples:')
            self.stdout.write('  python manage.py setup_firebase --test-file path/to/test.json')
            self.stdout.write('  python manage.py setup_firebase --prod-file path/to/prod.json')
            self.stdout.write('  python manage.py setup_firebase --test-file test.json --prod-file prod.json')
            self.stdout.write('  python manage.py setup_firebase --validate')
            return

        # Process test credentials
        if test_file:
            self._process_file(test_file, 'test')

        # Process prod credentials
        if prod_file:
            self._process_file(prod_file, 'prod')

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('\nSetup complete!'))
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Copy the environment variables above')
        self.stdout.write('2. Add them to your .env file')
        self.stdout.write('3. Restart your Django application')
        self.stdout.write('4. Run: python manage.py setup_firebase --validate')

    def _process_file(self, file_path, environment):
        """Process a single Firebase credentials file"""
        self.stdout.write(f'\n📄 Processing {environment.upper()} credentials...')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'✗ File not found: {file_path}'))
            return

        try:
            # Read JSON file
            with open(file_path, 'r') as f:
                cred_data = json.load(f)

            # Validate required fields
            required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email',
                             'client_id', 'auth_uri', 'token_uri', 'auth_provider_x509_cert_url',
                             'client_x509_cert_url']
            missing_fields = [field for field in required_fields if field not in cred_data]

            if missing_fields:
                self.stdout.write(self.style.ERROR(
                    f'✗ Missing required fields: {", ".join(missing_fields)}'
                ))
                return

            # Display results
            self.stdout.write(self.style.SUCCESS(f'✓ Valid Firebase credentials'))
            self.stdout.write(f'  Project ID: {cred_data.get("project_id")}')
            self.stdout.write(f'  Client Email: {cred_data.get("client_email")}')
            self.stdout.write('\nAdd these to your .env file:')

            env_prefix = f'FIREBASE_{environment.upper()}'

            # Generate environment variables
            env_vars = [
                f'{env_prefix}_TYPE={cred_data.get("type")}',
                f'{env_prefix}_PROJECT_ID={cred_data.get("project_id")}',
                f'{env_prefix}_PRIVATE_KEY_ID={cred_data.get("private_key_id")}',
                f'{env_prefix}_PRIVATE_KEY="{cred_data.get("private_key")}"',
                f'{env_prefix}_CLIENT_EMAIL={cred_data.get("client_email")}',
                f'{env_prefix}_CLIENT_ID={cred_data.get("client_id")}',
                f'{env_prefix}_AUTH_URI={cred_data.get("auth_uri")}',
                f'{env_prefix}_TOKEN_URI={cred_data.get("token_uri")}',
                f'{env_prefix}_AUTH_PROVIDER_CERT_URL={cred_data.get("auth_provider_x509_cert_url")}',
                f'{env_prefix}_CLIENT_CERT_URL={cred_data.get("client_x509_cert_url")}',
            ]

            self.stdout.write(self.style.WARNING('\n' + '\n'.join(env_vars)))

        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'✗ Invalid JSON file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error processing file: {e}'))
