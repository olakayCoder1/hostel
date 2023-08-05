from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from client.models import Booking
from django.contrib import messages

class HostelListMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path.startswith('/hostels') or request.path == '/': 
                booking = Booking.objects.filter(user=request.user).last()
                if booking and booking.expiration_date > timezone.now():
                    messages.info(request, 'Your booking has not expired yet. You cannot book another room.') 
                    return redirect(reverse('my-application'))  # Redirect to a page indicating expiration
                    
        response = self.get_response(request)
        return response
    
