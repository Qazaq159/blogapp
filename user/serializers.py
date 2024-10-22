from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'},
                                      label='Confirm password')

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']

    def validate(self, data):
        # Check that the two password fields match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        # Remove password2 since it's not needed for user creation
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
