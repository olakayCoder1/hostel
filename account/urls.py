from django.urls import path
from . import views


app_name = 'account' 


urlpatterns = [ 
    path('', views.AccountProfileView.as_view() , name='profile'),  
    path('info', views.AccountProfileInfoView.as_view() , name='profile_info'), 
    path('register', views.AccountRegisterView.as_view() , name='register'), 
    path('login', views.AccountLoginView.as_view(), name='login'), 
    path('logout', views.AccountLogoutView.as_view(), name='logout'), 
    path('activate', views.AccountActivationView.as_view(), name='activation'), 
    path('password-forget', views.ResetPasswordRequestEmailApiView.as_view(), name='forget_password'), 
    path('password-reset/<str:token>/<str:uuidb64>', views.SetNewPasswordTokenCheckApi.as_view(), name='set_password'), 
    path('password-change', views.AccountProfilePasswordView.as_view() , name='change_password'),  
]  