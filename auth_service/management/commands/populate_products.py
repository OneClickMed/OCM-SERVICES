from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from auth_service.models import Product


class Command(BaseCommand):
    help = 'Populate products and create user accounts with DRF tokens'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Creating product users and tokens...'))

        created_count = 0
        updated_count = 0

        for product_key, config in settings.PRODUCTS_CONFIG.items():
            try:
                # Create or get user for this product
                username = f"{product_key}_service"
                user, user_created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': f'{product_key}@service.internal',
                        'is_active': True,
                        'is_staff': False,
                    }
                )

                if user_created:
                    self.stdout.write(f'  Created user: {username}')

                # Create or get token for user
                token, token_created = Token.objects.get_or_create(user=user)

                if token_created:
                    self.stdout.write(f'  Generated token: {token.key}')
                else:
                    self.stdout.write(f'  Existing token: {token.key}')

                # Create or update product
                product, created = Product.objects.update_or_create(
                    name=product_key,
                    defaults={
                        'user': user,
                        'display_name': config['name'],
                        'test_tenant_id': config['test_tenant_id'],
                        'prod_tenant_id': config['prod_tenant_id'],
                        'is_active': True
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created product: {config["name"]}')
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Updated product: {config["name"]}')
                    )

                # Display token for easy copying
                self.stdout.write(
                    self.style.WARNING(f'  Token for {config["name"]}: {token.key}\n')
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error processing {product_key}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n{"="*60}\nCompleted! Created: {created_count}, Updated: {updated_count}\n{"="*60}'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '\nIMPORTANT: Save the tokens above. Use them in the Authorization header:\n'
                'Authorization: Token <your-token-here>'
            )
        )
