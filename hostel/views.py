from account.models import Transaction
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User ,Transaction
from client.models import Booking, Compound
from django.conf import settings
import requests


class VerifyPayment(APIView):

    def get(self,request):
        transaction_reference = request.GET.get('reference')
        if not transaction_reference:
            return Response({'status':False, 'detail':'Reference not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize Paystack API endpoint and headers
        paystack_verify_url = f"https://api.paystack.co/transaction/verify/{transaction_reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }
        # Make the API call to verify the payment
        response = requests.get(paystack_verify_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data['data']['status'] == 'success':
                transaction = Transaction.objects.filter(reference=transaction_reference).first()
                transaction.status = 'success'
                transaction.save()
                # Payment was successful, update your database or perform any other actions
                return Response({'status':True, 'detail':'Payment successful. Thank you!'}, status=status.HTTP_200_OK)
            else:
                transaction = Transaction.objects.filter(reference=transaction_reference).first()
                transaction.status = 'failed'
                transaction.save()
                return Response({'status':False, 'detail':'Payment failed.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False, 'detail':'Error verifying payment.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class InitiatePayment(APIView):
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({"status": False, 'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        compound_id = request.GET.get('compound_id')
        if not compound_id:
            return Response({'status':False, 'detail':'Compound ID not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        compound = Compound.objects.filter(uuid=compound_id).first()
        if not compound:
            return Response({'status':False, 'detail':'Compound not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not compound.is_active:
            return Response({'status':False, 'detail':'Compound is not active'}, status=status.HTTP_400_BAD_REQUEST)
        
        if compound.get_remaining_capacity <= 0:
            return Response({'status':False, 'detail':'Compound is full'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        transaction = Transaction(
            user=request.user, amount=30000.00,
            compound=compound
        )
        transaction.save()

        response_data = {
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
            'reference': transaction.reference,
            'amount': transaction.amount * 100,
            'email': user.email
        }

        return Response({'status':True, 'data':response_data}, status=status.HTTP_200_OK)

 