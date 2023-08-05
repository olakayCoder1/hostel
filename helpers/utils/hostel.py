from client.models import ( Compound, Room , Hostel, Booking, Document , Accomodation)
from account.models import User



class HostelManager:


    def __init__(self, request):
        self.request = request



    def get_hostel(self, id):    
        return Hostel.objects.get(uuid=id)
    

    def get_open_disabled_compounds(self, hostel):  

        return Compound.objects.filter(hostel=hostel, is_active=True, has_disable=True)
    

    def get_available_hostel(self):  
        context = None
        auth_user = User.objects.get(id=self.request.user.id)
        if auth_user.gender == 'male':
            if auth_user.profile.is_disabled:
                context = Hostel.objects.filter(category_type='male', is_active=True , has_disable=True) 
            else: 
                context = Hostel.objects.filter(category_type='male', is_active=True) 
        else:
            if auth_user.profile.is_disabled:
                context = Hostel.objects.filter(category_type='male', is_active=True , has_disable=True)
            else:
                context = Hostel.objects.filter(category_type='female', is_active=True)

        return context
    
    def get_open_compounds(self, hostel):  
        result = []
        compounds = Compound.objects.filter(hostel=hostel)
        auth_user = User.objects.get(id=self.request.user.id)
        for compound in compounds:
            if auth_user.profile.is_disabled:
                if compound.has_open_disabled_rooms:
                    result.append(compound)
            else:
                if compound.get_open_rooms > 0:
                    result.append(compound)
        return result
    
