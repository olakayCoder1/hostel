from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from client.models import Booking
from account.models import User
from helpers.main import Injector
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User ,Transaction
from django.utils import timezone

class StudentCheckIn(APIView):
     
    def post(self, request):
        auth_user = User.objects.get(id=request.user.id)

        access_code = request.data.get('access_code')

        if not access_code:
            return Response({'status':False, 'detail':'Provide access code'}, status=status.HTTP_400_BAD_REQUEST)

        if not auth_user.profile.is_staff:
            return Response({'status':False, 'detail':'You do not have access'}, status=status.HTTP_403_FORBIDDEN)
        
        booking = Booking.objects.filter(access_code=access_code).first()

        if not booking:
            return Response({'status':False, 'detail':'Invalid access code'}, status=status.HTTP_400_BAD_REQUEST)
        
        if booking.expiration_date < timezone.now():
            return Response({'status':False, 'detail':'Access code has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        return Response({'status':True, 'detail':'Verification successfull. Access code is valid'}, status=status.HTTP_200_OK)   