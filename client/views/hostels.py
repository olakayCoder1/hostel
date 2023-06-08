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
        hostels = [ 1,2,3,4,5,6,7,8,9]
        hostels = HostelCategory.objects.filter(is_active=True)
        return render(request, 'client/hostels.html' , context)  


class HostelDetailsView(View):

    def get(self, request , id):
        try:
            hostel = Hostel.objects.get(uuid=id)
        except Hostel.DoesNotExist:
            return render(request, 'client/hostel_details.html')
        context = {
            'hostel': hostel,
            'compound': hostel.get_compounds(),

        }
        return render(request, 'client/hostel_details.html' )  






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
