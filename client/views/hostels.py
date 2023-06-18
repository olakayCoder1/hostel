from django.views import View
from django.shortcuts import render
from client.models import ( HostelCategory, Compound, Room , Hostel, Booking, Document )
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import User


class HostelsView(LoginRequiredMixin, View):

    def get(self, request):
        auth_user = User.objects.get(id=request.user.id)
        context = {}
        if auth_user.gender == 'male':
            context['hostels'] = Hostel.objects.filter(hostel_category__name='Male') 
        else:
            context['hostels'] = Hostel.objects.filter(hostel_category__name='Female') 
        return render(request, 'client/hostels.html' , context)  


class HostelDetailsView(View):

    def get(self, request , id):
        hostel = Hostel.objects.get(uuid=id)
        print(hostel.name) 
        context = {
            'hostel' : hostel,
            'hostel_name' : hostel.name,
            'compounds': hostel.get_compounds,
            'compounds_count': hostel.get_compound_count,
            'active_compounds_count': hostel.get_active_compound_count,
            'rooms_count': hostel.get_room_count,
            'open_rooms_count': hostel.get_open_rooms
            
        }
        
        return render(request, 'client/hostel_details.html' ,context)  





class CompoundDetailsView(View):

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
            'open_rooms_count': hostel.get_open_rooms
            
        }
        
        return render(request, 'client/hostel_compound_details.html' ,context)   






class HostelApplicationView(View):

    def get(self, request):
        return render(request, 'client/hostel_application.html')


    def post(self, request):
        return render(request, 'client/hostel_application.html')
    



class HostelAccreditationView(View):

    def get(self, request):
        return render(request, 'client/hostel_accreditation.html')


    def post(self, request):
        return render(request, 'client/hostel_application.html')
