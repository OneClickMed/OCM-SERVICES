from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'user', 'is_active', 'created_at')
    list_filter = ('is_active', 'name')
    search_fields = ('name', 'display_name', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'get_token')

    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'display_name', 'user', 'is_active')
        }),
        ('Authentication', {
            'fields': ('get_token',),
            'description': 'Use this token in API requests: Authorization: Token <token>'
        }),
        ('Firebase Configuration', {
            'fields': ('test_tenant_id', 'prod_tenant_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_token(self, obj):
        """Display the DRF token for this product"""
        return obj.token.key if obj.id else 'Token will be generated after saving'
    get_token.short_description = 'API Token'
