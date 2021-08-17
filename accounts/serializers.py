from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True
    )

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        username = attrs.get('username', None)
        if username is None:
            raise serializers.ValidationError("username is None.")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("username is exist.")

        email = attrs.get("email", None)
        if email is None:
            raise serializers.ValidationError("email is None.")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("email is exist.")

        return attrs
