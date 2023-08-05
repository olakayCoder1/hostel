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
from django.shortcuts import render , redirect , reverse 
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from django.contrib.auth import authenticate , login as auth_login , logout as auth_logout
from django.contrib.auth.decorators import login_required
from rest_framework import status  , generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied , NotAuthenticated
from account.models import User , Profile , ActivationToken
from account.forms import AccountRegisterForm 
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




class ResetPasswordRequestEmailApiView(View):
    """
    This view handle sending of reset password link to user email
    """
    def get(self, request):
        return render(request, 'account/forget_password.html')

    def post(self, request):
        email = request.data.get('email', None)

        if not email:
            messages.error(request, 'Please fill all fields')
            return render(request, 'account/forget_password.html')
        try:
            user = User.objects.get(email=email)
            Thread(target=MailServices.forget_password_mail, kwargs={ 'user': user }).start()
            messages.success(request, 'Password reset instruction will be sent to the mail')
            return render(request, 'account/forget_password.html')
        except:
            messages.success(request, 'Email does not exist')
            return render(request, 'account/forget_password.html')



class SetNewPasswordTokenCheckApi(View):
    """
    This view handle changing of user password on forget password
    """

    def get(self,request):
        return render(request, 'account/set_password.html')


    def post(self, request, token , uuidb64 ):
        try:
            id = smart_str(urlsafe_base64_decode(uuidb64))
            user = User.objects.get(id=id)
            password1 = request.data.get('password1',None)
            password2 = request.data.get('password2',None)
            if password1 != password2 :
                messages.error(request, 'Password does not match')
                return render(request, 'account/set_password.html')
            
            if PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(password1)
                user.save() 
                messages.success(request, 'Password updated successfully')
                return redirect('account:login')
            
            messages.error(request, 'Invalid token')
            return render(request, 'account/set_password.html')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Invalid token')
            return render(request, 'account/set_password.html')



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



class AccountRegisterView(View):

    def get(self, request):
        return render(request, 'account/register.html')
    
    def post(self, request):
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        disable = request.POST.get('disable', None)
        gender = request.POST.get('gender' , None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)

        if ( not first_name or not last_name or not email or \
            not disable or not gender or not password or not password2):
            messages.error(request, 'Please fill all fields')
            return render(request, 'account/register.html')

        # validate password match
        if password != password2:
            messages.error(request, 'Password does not match')
            return render(request, 'account/register.html')

        # validation for unilorin student mail
        email_pattern = r'^[a-zA-Z0-9._%+-]+@unilorin\.com$'

        if True:
        # if re.match(email_pattern, email):
            user_exist = User.objects.filter(email=email).exists()
            if user_exist:
                messages.error(request, 'Student already exist')
                return render(request, 'account/register.html')
            else:
                new_user = User.objects.create_user( 
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    is_active=False,
                )
                new_user.save()
                if disable == "yes":
                    profile = Profile.objects.filter(user__id=new_user.id).first()
                    profile.is_disabled
                    profile.save()
                token = uuid4().hex
                activation_base = request.build_absolute_uri(reverse('account:activation'))
                acivation_token = ActivationToken.objects.create(user=new_user, token_type='account', token=token)
                messages.success(request, 'Account activation link has been sent to your mail')
                Thread(target=MailServices.send_account_activation_mail, kwargs={ 
                    'user': new_user, 'token':token , 'url' : activation_base }).start()
                return redirect('account:login')

        return render(request, 'account/register.html')




class AccountActivationView(View):
    """
    This view handle account activation
    """

    def get(self, request):
        uuidb64 = request.GET.get('safe',None)
        token = request.GET.get('token',None)
        
        if not token or not uuidb64: 
            messages.error(request, 'Invalid account activation link')
            return redirect('account:register')
        try:
            id = smart_str(urlsafe_base64_decode(uuidb64))
            user = User.objects.get(id=id)
            token_obj = ActivationToken.objects.filter(user=user, token=token, token_type='account').first()
            print(token_obj)
            if not token_obj:
                print('***'*100)
                print(uuidb64)
                print(token) 
                print('***'*100)
                messages.error(request, 'Invalid account activation link')
                return redirect('account:register')
            token_obj.is_used = True
            token_obj.save()
            user.email_verified = True
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated- Login to continue')
            return redirect('account:login')
        except:

            messages.error(request, 'Invalid account activation link')
            return redirect('account:register')



class AccountLogoutView(View):

    def get(self, request):
        auth_logout(request)
        return redirect('account:login')


# http://127.0.0.1:8000/account/login?/account/password-change=/account/password-change

class AccountLoginView(View):

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.error(request, 'Please fill all fields')
            return render(request, 'account/login.html') 
        if is_valid_email(email): 
            user = authenticate(email=email , password=password)
            if user:
                if user.is_active:
                    redirect_url = request.GET.get('next', '/') 
                    auth_login(request, user)
                    return redirect(redirect_url) 
                else:
                    messages.error(request, 'Your account is disabled, kindly contact the administrative')
                    return render(request, 'account/login.html') 

            else:
                messages.error(request, 'Invalid login credential') 
                return render(request, 'account/login.html')  

        else:
            messages.error(request, 'Invalid email address')
            return render(request, 'account/login.html') 
        


    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account:profile') 
        return render(request, 'account/login.html')





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
