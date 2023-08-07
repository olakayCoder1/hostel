from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from client.models import Hostel
from account.models import User
from helpers.main import Injector


class DashboardView(LoginRequiredMixin, View,Injector):
     
    def get(self, request):
        auth_user = User.objects.get(id=request.user.id)

        

        context = self.get_inject_context()


        if auth_user.profile.is_staff:
            return render(request, 'test/checkin.html', context ) 
        auth_user = User.objects.get(id=self.request.user.id)
        if auth_user.gender == 'male':
            context['hostels'] = Hostel.objects.filter(category_type='male', is_active=True) 
        else:
            context['hostels'] = Hostel.objects.filter(category_type='female', is_active=True) 
        return render(request, 'client/home.html', context )   
    
