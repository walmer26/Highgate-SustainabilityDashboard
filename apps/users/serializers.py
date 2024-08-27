from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=254)
    email = serializers.EmailField(max_length=254)
    fullname = serializers.SerializerMethodField(method_name='get_full_name')
    active = serializers.BooleanField(source='is_active')
    staff = serializers.BooleanField(source='is_staff')
    superuser = serializers.BooleanField(source='is_superuser')
    last_login = serializers.DateTimeField(format="%d/%b/%Y %H:%M:%S")

    def get_full_name(self, user: User):
        return user.first_name + " " + user.last_name