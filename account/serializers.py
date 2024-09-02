from rest_framework import serializers
from django.contrib.auth.models import User

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', "email", "password")

        extra_kwargs = {
            'first_name': { 'required': True, "allow_blank": False },
            'last_name': { 'required': True, "allow_blank": False },
            'email': { 'required': True, "allow_blank": False },
            'password': { 'required': True, "allow_blank": False, 'min_length': 6 },
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
       model = User
       fields = ('first_name','last_name',"username", "email") 


from rest_framework import serializers
from .models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'timestamp']
        read_only_fields = ['from_user', 'status', 'timestamp']

from rest_framework import serializers
from django.contrib.auth.models import User

class FriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

