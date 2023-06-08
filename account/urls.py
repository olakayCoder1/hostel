from django.urls import path
from . import views


app_name = 'account' 


urlpatterns = [ 
    path('', views.AccountProfileView.as_view() , name='profile'),  
    path('info', views.AccountProfileInfoView.as_view() , name='profile_info'), 
    path('register', views.register , name='register'), 
    path('login', views.AccountLoginView.as_view(), name='login'), 
    path('logout', views.AccountLogoutView.as_view(), name='logout'), 
    path('password-forget', views.forget_password, name='forget_password'), 
    path('password-reset/<str:token>/<str:uuidb64>', views.set_password, name='set_password'), 
    path('password-change', views.AccountProfilePasswordView.as_view() , name='change_password'),  
]  