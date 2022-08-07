from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'pkid', 'id', 'email', 'name', 'password', 'is_staff',
            'is_active', 'created')

    def create(self, validated_data):
        # TODO do i really need to do this?
        return User.objects.create_user(**validated_data)