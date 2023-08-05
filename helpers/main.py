from client.models import Hostel
from account.models import User

class Injector:

    context = {}
    def __init__(self, request) -> None:
        self.request = request

    def get_inject_context(self):
        if self.request.user.is_authenticated:
            auth_user = User.objects.get(id=self.request.user.id)
            if auth_user.gender == 'male':
                self.context['nav_hostels'] = Hostel.objects.filter(category_type='male') 
            else:
                self.context['nav_hostels'] = Hostel.objects.filter(category_type='female') 

        return self.context