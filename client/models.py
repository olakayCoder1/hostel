from django.db import models
from django.utils.translation import gettext_lazy as _
import secrets
import string


class Hostel(models.Model):
    CATEGORY_TYPE = (
        ('male','Male'),
        ('female','Female')
    )
    category_type = models.CharField(max_length=255 , blank=True, null=True , choices=CATEGORY_TYPE)
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='hostels', blank=True, null=True)
    has_disable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

    @property
    def get_compound_count(self):
        """Returns the number of compounds in this hostel"""
        return self.compound_set.count()
    
    @property
    def get_active_compound_count(self):
        """Returns the number of compounds in this hostel"""
        return self.compound_set.filter(is_active=True).count()
    
    @property
    def get_room_count(self):
        """Returns the number of rooms in this hostel"""
        return Room.objects.filter(hostel__id=self.id).count()
    
    @property
    def get_room_capacity_count(self):
        """Returns the number of beds in this hostel"""
        return self.rooms.aggregate(models.Sum('capacity'))['capacity__sum']
    
    @property
    def get_open_rooms(self):
        """Returns the number of rooms in this hostel"""
        return Room.objects.filter(hostel__id=self.id,is_active=True).count() 
    
    @property
    def get_compounds(self):
        """Returns the number of rooms in this hostel"""
        return self.compound_set.all()  
    
    @property
    def get_rooms(self):
        """Returns the number of rooms in this hostel"""
        return self.rooms.all()


    @classmethod
    def get_open_hostel(cls):
        """Returns the number of available bed space in this hostel"""
        result = [ hostel for hostel in cls.objects.filter(is_active=True) if hostel.get_open_rooms > 0 ] 
        return result
    





class Compound(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    name = models.CharField(max_length=255)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='compounds', blank=True, null=True) 
    is_active = models.BooleanField(default=True)
    has_disable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.hostel.name} - { self.name}"
    
    @property
    def get_room_count(self):
        """Returns the number of rooms in this compound"""
        return self.rooms.count()
    

    @property
    def get_room_capacity_count(self):
        """Returns the number of beds in this compound"""
        return self.rooms.aggregate(models.Sum('capacity'))['capacity__sum']
    
    @property
    def get_open_rooms(self):
        """Returns the number of rooms in this compound"""
        return Room.objects.filter(compound=self,is_active=True).count()

    def get_rooms(self):
        """Returns the number of rooms in this compound"""
        return Room.objects.filter(compound=self)
    
    @property
    def get_remaining_capacity(self):
        """Returns the number of available bed space in this compound"""
        return (
            (Room.objects.filter(compound=self).aggregate(models.Sum('capacity'))['capacity__sum']) -
             ( Room.objects.filter(compound=self).aggregate(models.Sum('book_count'))['book_count__sum'])
        )

    @property
    def has_open_disabled_rooms(self):
        """Returns the number of available bed space in this compound"""
        return Room.objects.filter(compound=self,is_active=True, is_disabled=True).count() > 0
    

    @property
    def get_open_disabled_rooms(self):
        """Returns the number of available rooms in this compound for disabled students"""
        return Room.objects.filter(compound=self, is_active=True, is_disabled=True).count()
    


    @classmethod
    def get_open_compounds(cls):
        """Returns the number of available bed space in this compound"""
        return cls.objects.filter(get_open_rooms__gt=0)



class Room(models.Model):
    """
    This model represents a hostel -> compound -> room
    """
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(
        default=4,
        help_text=_("The number of students this room can accommodate")
    )
    floor = models.IntegerField(
        default=1,
        help_text=_("The floor number of the room"),
    )
    hostel = models.ForeignKey(
        Hostel, 
        on_delete=models.CASCADE,
        help_text=_("The hostel this room belongs to"),
    )
    compound = models.ForeignKey(
        Compound, 
        on_delete=models.CASCADE,
        help_text=_("The compound this room belongs to")
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Whether this room is active or not")
    )
    book_count = models.IntegerField(
        default=0,
        help_text=_("The number of times this room has been booked")
    )
    is_disabled = models.BooleanField(
        default=False,
        help_text=_("Whether this room is disabled or not")
    )
    image = models.ImageField(upload_to='rooms', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.hostel.name} - { self.compound.name } {self.name}"
    
    @property
    def get_remaining_capacity(self):
        return self.capacity - self.book_count






def upload_to(instance, filename):
    return 'booking/{filename}'.format(filename=filename)

class Booking(models.Model):
    """
    This model represents a booking
    """
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    )
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    hostel = models.ForeignKey('client.Hostel', on_delete=models.CASCADE)
    compound = models.ForeignKey('client.Compound', on_delete=models.CASCADE)
    room_code = models.CharField(max_length=100, null=True, blank=True)
    qr_code = models.ImageField( 
        upload_to=upload_to , null=True , blank=True ,
    )
    status = models.CharField(max_length=10, default='pending')
    payment_status = models.CharField(max_length=10, default='pending')
    transaction = models.OneToOneField('account.Transaction', on_delete=models.CASCADE, null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    access_code = models.CharField(null=True, max_length=10)



    def __str__(self) -> str:
        return f"{self.user.email} : {self.hostel.name} - {self.compound.name}"



    @classmethod
    def generate_access(cls):
        characters = string.ascii_letters + string.digits 
        length = 10
        access = ''.join(secrets.choice(characters) for _ in range(length))
        ref_exist = cls.objects.filter(access_code=access).exists()
        if not ref_exist:
            return access
        else:
            cls.generate_access()



class Document(models.Model):
    """
    This model represents a document
    """
    DOCUMENT_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),   
    )
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class Accomodation(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    access_code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
