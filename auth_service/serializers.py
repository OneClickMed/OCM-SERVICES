from rest_framework import serializers
from email_validator import validate_email, EmailNotValidError


class GenericEmailSerializer(serializers.Serializer):
    """Serializer for generic email sending"""
    to_email = serializers.EmailField(required=True)
    subject = serializers.CharField(required=True, max_length=255)
    html_content = serializers.CharField(required=True)
    text_content = serializers.CharField(required=False, allow_blank=True)
    environment = serializers.ChoiceField(choices=['test', 'prod'], default='prod')

    def validate_to_email(self, value):
        """Validate email format"""
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise serializers.ValidationError(str(e))
        return value


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset request"""
    email = serializers.EmailField(required=True)
    environment = serializers.ChoiceField(choices=['test', 'prod'], default='prod')
    user_name = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        """Validate email format"""
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise serializers.ValidationError(str(e))
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer for forgot password request"""
    email = serializers.EmailField(required=True)
    environment = serializers.ChoiceField(choices=['test', 'prod'], default='prod')
    user_name = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        """Validate email format"""
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise serializers.ValidationError(str(e))
        return value


class EmailVerificationSerializer(serializers.Serializer):
    """Serializer for email verification request"""
    email = serializers.EmailField(required=True)
    environment = serializers.ChoiceField(choices=['test', 'prod'], default='prod')
    user_name = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        """Validate email format"""
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise serializers.ValidationError(str(e))
        return value


class WelcomeEmailSerializer(serializers.Serializer):
    """Serializer for welcome email request"""
    email = serializers.EmailField(required=True)
    environment = serializers.ChoiceField(choices=['test', 'prod'], default='prod')
    user_name = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        """Validate email format"""
        try:
            validate_email(value)
        except EmailNotValidError as e:
            raise serializers.ValidationError(str(e))
        return value


class VerifyEmailConfirmationSerializer(serializers.Serializer):
    """Serializer for email verification confirmation"""
    token = serializers.CharField(required=True)
    environment = serializers.ChoiceField(choices=['test', 'prod'], default='prod')


class EmailResponseSerializer(serializers.Serializer):
    """Serializer for email operation response"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    email_log_id = serializers.IntegerField(required=False)
    data = serializers.DictField(required=False)
