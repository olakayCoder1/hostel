from datetime import datetime
import time
from threading import Thread
from uuid import uuid4
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.shortcuts import render , redirect
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from django.contrib.auth import authenticate , login as auth_login , logout as auth_logout
from django.contrib.auth.decorators import login_required
from rest_framework import status  , generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied , NotAuthenticated
from account.models import User 
from .serializers import ( 
    SignupSerializer,  LoginSerializer,
    ResetPasswordRequestEmailSerializer, 
    SetNewPasswordSerializer, 
    ChangePasswordSerializer  
)
from helpers.libs.tokens import create_jwt_pair_for_user
from helpers.libs.mails import MailServices



def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False



class SignupApiView(generics.GenericAPIView):
    """
    This view handle user registration
    """
    serializer_class = SignupSerializer

    def post(self, request , *args, **kwarg):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(): 
            # check if email already exists
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({'success':False,'detail': 'Email already exists'} , status=status.HTTP_400_BAD_REQUEST)
            
            genders = ['male', 'female']
            if serializer.validated_data['gender'] not in genders: 
                response = {
                    'success': False,
                    'detail': f"Gender value should be among {genders}"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            

            new_user = User()
            new_user.first_name = serializer.validated_data['first_name']
            new_user.last_name = serializer.validated_data['last_name']
            new_user.email = serializer.validated_data['email']
            new_user.set_password(str(serializer.validated_data['password']))
            try:
                tokens = create_jwt_pair_for_user(new_user)
                new_user.save()
                return Response({
                    'success':True,
                    'detail': 'Account created successfully',
                    'data': {
                        'tokens': tokens,
                    }, 

                } , status=status.HTTP_200_OK)
            except:
                return Response({'success':False,'detail': 'Error occurred creating account'} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':False,'detail': serializer.errors} , status=status.HTTP_400_BAD_REQUEST)




class LoginApiView(generics.GenericAPIView):
    """
    This view handle user login
    """
    serializer_class = LoginSerializer
  
    
    def post(self, request ):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True): 
            email = serializer.validated_data['email'] 
            password = serializer.validated_data['password']
            user = authenticate(email=email , password=password)
            if user:

                if user.is_active:
                    tokens = create_jwt_pair_for_user(user)
                    response = {
                        'success': True ,
                        'detail': 'Login is successful',
                        'data': {
                        'tokens': tokens,
                        },
                    }
                    return Response(response , status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied(
                            "Your account is disabled, kindly contact the administrative")
            
            return Response({'success': False , 'detail': 'Invalid login credential'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer_error_response = {
            "success": False,
            "detail": serializer.errors
        }
        return Response(serializer_error_response, status=status.HTTP_400_BAD_REQUEST)




class ResetPasswordRequestEmailApiView(generics.GenericAPIView):
    """
    This view handle sending of reset password link to user email
    """
    serializer_class = ResetPasswordRequestEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                Thread(target=MailServices.forget_password_mail, kwargs={ 'user': user }).start()
                return Response( 
                        {'success':True , 'detail': 'Password reset instruction will be sent to the mail' },
                        status=status.HTTP_200_OK
                        )
            except:
                return Response( 
                    {'success':True , 'detail': 'Password reset instruction will be sent to the mail' }, 
                    status=status.HTTP_200_OK
                    )
        return Response( 
                    {'success':False , 'detail': serializer.errors },  
                    status=status.HTTP_400_BAD_REQUEST
                    )



class SetNewPasswordTokenCheckApi(generics.GenericAPIView):
    """
    This view handle changing of user password on forget password
    """
    serializer_class = SetNewPasswordSerializer


    def post(self, request, token , uuidb64 ):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                id = smart_str(urlsafe_base64_decode(uuidb64))
                user = User.objects.get(id=id)
                password1 = serializer.validated_data['password1']
                password2 = serializer.validated_data['password2']
                if password1 != password2 :
                    return  Response({'success':False ,'detail': 'Password does not match'} , status=status.HTTP_400_BAD_REQUEST)
                if PasswordResetTokenGenerator().check_token(user, token):
                    data = request.data
                    serializer = self.serializer_class(data=data)
                    serializer.is_valid(raise_exception=True)
                    user.set_password(serializer.validated_data['password1'])
                    user.save() 
                    return Response({'success':True , 'detail':'Password updated successfully'}, status=status.HTTP_200_OK)
                return Response({'success':False ,'detail':'Token is not valid'}, status=status.HTTP_400_BAD_REQUEST)
            except DjangoUnicodeDecodeError as identifier:
                return Response({'success':False ,'detail': 'Token is not valid'}, status=status.HTTP_400_BAD_REQUEST)



#  This view handle password update within app ( authenticated user)
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer 
    permission_classes = [ IsAuthenticated ] 
    model = User

    def get_object(self,queryset=None):
        obj = self.request.user
        return obj
    

    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            password1 = serializer.validated_data['password1']
            password2 = serializer.validated_data['password2']
            if password1 != password2 :
                return  Response({'success':False ,'detail': 'Password does not match'} , status=status.HTTP_400_BAD_REQUEST)
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'success':False ,'detail': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("password2"))
            self.object.save()
            response={
                'success': True,
                'detail': 'Password updated successfully',
                }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AccountLogoutView(View):

    def get(self, request):
        auth_logout(request)
        return redirect('account:login')


# http://127.0.0.1:8000/account/login?/account/password-change=/account/password-change

class AccountLoginView(View):

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        if not email or not password:
            messages.error(request, 'Please fill all fields')
        if is_valid_email(email): 
            user = authenticate(email=email , password=password)
            if user:
                if user.is_active:
                    redirect_url = request.GET.get('next', '/') 
                    auth_login(request, user)
                    return redirect(redirect_url) 
                
                else:
                    messages.error(request, 'Your account is disabled, kindly contact the administrative')

            else:
                messages.error(request, 'Invalid login credential')  

        else:
            messages.error(request, 'Invalid email address')
        
        return render(request, 'account/login.html') 


    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account:profile') 
        return render(request, 'account/login.html')




def register(request):
    return render(request, 'account/register.html')

def forget_password(request):
    return render(request, 'account/forget_password.html')

def set_password(request, token , uuidb64):
    return render(request, 'account/set_password.html')



class AccountProfileView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'account/profile.html')





class AccountProfileInfoView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'account/account_info.html')
    


class AccountProfilePasswordView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'account/change_password.html')



def change_password(request):
    return render(request, 'account/change_password.html')
