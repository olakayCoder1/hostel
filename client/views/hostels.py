from django.views import View
from django.shortcuts import render, reverse, redirect
from django.db.models import Count
from client.models import ( Compound, Room , Hostel, Booking, Document , Accomodation)
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import User
from helpers.main import Injector
from helpers.utils.hostel import HostelManager
from django.conf import settings

class HostelsView(LoginRequiredMixin , View,HostelManager, Injector):

    def get(self, request):
        context = self.get_inject_context()
        auth_user = User.objects.get(id=request.user.id)

        has_booked = Accomodation.objects.filter(user__id=request.user.id, is_active=True).exists()
        if has_booked:
            context['has_booked'] = True
            return render(request, 'client/hostels.html' , context)
        
        context['hostels'] = self.get_available_hostel()
        return render(request, 'client/hostels.html' , context)  



class HostelDetailsView(LoginRequiredMixin,View , HostelManager,Injector ):

    def get(self, request , id):
        # get_open_compounds
        hostel = Hostel.objects.get(uuid=id)
        context = self.get_inject_context() 

        payent_initialise_url = reverse('initiate_payment')

        print(payent_initialise_url)
        context.update({
            "payment_public_key": settings.PAYSTACK_PUBLIC_KEY,
            'hostel' : hostel,
            'hostel_name' : hostel.name,
            'compounds': self.get_open_compounds(hostel),
            'compounds_count': hostel.get_compound_count,
            'active_compounds_count': hostel.get_active_compound_count,
            'rooms_count': hostel.get_room_count,
            'open_rooms_count': hostel.get_open_rooms
        })
        
        return render(request, 'client/hostel_details.html' ,context)  





class CompoundDetailsView(LoginRequiredMixin,View,Injector):

    def get(self, request , hostel_id, compound_id ):
        hostel = Hostel.objects.get(uuid=hostel_id)

        compound = Compound.objects.filter(uuid=compound_id, hostel__uuid=hostel_id).first() 
        print(compound.name) 
        payent_initialise_path = reverse('initiate_payment')
        payent_initialise_url = request.build_absolute_uri(payent_initialise_path)
        print(payent_initialise_url)
        page_name = f"{hostel.name} : {compound.name}" 
        context = {
            "payment_public_key": settings.PAYSTACK_PUBLIC_KEY,
            'payent_initialise_url': payent_initialise_url,
            'page_name' : page_name,
            'hostel' : hostel,
            'compound' : compound,
            'hostel_name' : hostel.name,
            'compounds': hostel.get_compounds,
            'compounds_count': hostel.get_compound_count,
            'active_compounds_count': hostel.get_active_compound_count,
            'rooms_count': hostel.get_room_count,
            'open_rooms_count': hostel.get_open_rooms,
            'open_rooms': hostel.get_open_rooms
            
        }
        
        return render(request, 'client/hostel_compound_details.html' ,context)   






class HostelApplicationView(LoginRequiredMixin,View,Injector):

    def get(self, request):
        return render(request, 'client/hostel_application.html')


    def post(self, request):
        return render(request, 'client/hostel_application.html')
    



class HostelAccreditationView(LoginRequiredMixin,View,Injector):

    def get(self, request):
        return render(request, 'client/hostel_accreditation.html')


    def post(self, request):
        return render(request, 'client/hostel_application.html')
