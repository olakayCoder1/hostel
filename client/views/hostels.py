from django.views import View
from django.shortcuts import render
from client.models import ( HostelCategory, Compound, Room , Hostel, Booking, Document )
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import User
from helpers.main import Injector

class HostelsView(LoginRequiredMixin , View, Injector):

    def get(self, request):
        auth_user = User.objects.get(id=request.user.id)
        from django.db.models import Count
 
        hostel_categories = HostelCategory.objects.annotate(compound_count=Count('compound'), room_count=Count('room')) 

        for n in hostel_categories:
            print(n.compound_count, n.room_count, n.name)  

        context = self.get_inject_context()
        auth_user = User.objects.get(id=self.request.user.id)
        if auth_user.gender == 'male':
            context['hostels'] = Hostel.objects.filter(hostel_category__name='Male', is_active=True) 
        else:
            context['hostels'] = Hostel.objects.filter(hostel_category__name='Female', is_active=True) 
        return render(request, 'client/hostels.html' , context)  



class HostelDetailsView(LoginRequiredMixin,View , Injector ):

    def get(self, request , id):
        hostel = Hostel.objects.get(uuid=id)
        context = self.get_inject_context() 
        context.update({
            'hostel' : hostel,
            'hostel_name' : hostel.name,
            'compounds': hostel.get_compounds,
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

        page_name = f"{hostel.name} : {compound.name}" 
        context = {
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
