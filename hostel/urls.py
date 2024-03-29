"""
URL configuration for hostel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from client.views.clients import DashboardView
from client.views.staff import StudentCheckIn
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    path('account/', include('account.urls')),
    path('hostels/', include('client.urls.hostels')),  
    path('myspace/', MyApplication.as_view(), name='my-application'),  
    # path('hostels/', InitiatePayment.as_view(), name='initiate-payment'),  
    path('initiate_payment',InitiatePayment.as_view(), name='initiate_payment'), 
    path('verify_payment', VerifyPayment.as_view(), name='verify_payment'),
    path('validate_code', VerifyPayment.as_view(), name='validate_code'),
    path('student/checkin', StudentCheckIn.as_view(), name='student_checkin'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)