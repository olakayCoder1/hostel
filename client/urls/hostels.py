from django.urls import path
from client.views.hostels import (
    HostelApplicationView , 
    HostelAccreditationView,
    HostelsView,
    HostelDetailsView    ,
    CompoundDetailsView
)

 
app_name = 'hostels'

urlpatterns = [ 
    path('', HostelsView.as_view(), name='hostels'), 
    path('<str:id>', HostelDetailsView.as_view(), name='hostel_details'), 
    path('<str:hostel_id>/<str:compound_id>', CompoundDetailsView.as_view(), name='compound_details'), 
    path('applications', HostelApplicationView.as_view(), name='hostel_application'), 
    path('accreditation', HostelAccreditationView.as_view(), name='hostel_accreditation'), 
]