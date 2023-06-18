from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from client.models import Hostel
from account.models import User
from helpers.main import Injector


class DashboardView(LoginRequiredMixin, View,Injector):
     
    def get(self, request):
        auth_user = User.objects.get(id=request.user.id)

        self.context['hostels'] = Hostel.objects.all()
        return render(request, 'client/home.html', ) 