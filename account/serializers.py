from rest_framework import serializers
from account.models import User




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)



class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)
    gender = serializers.CharField(allow_blank=False)
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)  




"""
!!! USER PASSWORD MANAGEMENT SERIALIZER START
"""
class ResetPasswordRequestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields =  ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length=1,max_length=30, write_only=True , style={'input-type': 'password'} )
    password2 = serializers.CharField(min_length=1,max_length=30, write_only=True , style={'input-type': 'password'} )
    
    class Meta:
        fields = ['password', 'password2']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True , style={'input-type': 'password'} )
    password1 = serializers.CharField(required=True , style={'input-type': 'password'} )
    password2 = serializers.CharField(required=True , style={'input-type': 'password'} )
