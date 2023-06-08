from django.db import models
from django.utils.translation import gettext_lazy as _




class HostelCategory(models.Model):
    """
    This model represents a hostel
    """
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255 , blank=True, null=True) 
    description = models.TextField( blank=True, null=True)
    image = models.ImageField(upload_to='hostel_type', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


    @property
    def get_compound_count(self):
        """Returns the number of compounds in this hostel category"""
        return self.compounds.count()
    
    @property
    def get_room_count(self):
        """Returns the number of rooms in this hostel category"""
        return self.rooms.count()
    
    @property
    def get_room_capacity_count(self):
        """Returns the number of beds in this hostel"""
        return self.rooms.aggregate(models.Sum('capacity'))['capacity__sum']
    
    @property
    def get_open_rooms(self):
        """Returns the number of rooms in this hostel"""
        return self.rooms.filter(is_active=True).count()
    
    def get_compounds(self):
        """Returns the number of rooms in this hostel"""
        return self.compounds.all()
    
    def get_rooms(self):
        """Returns the number of rooms in this hostel"""
        return self.rooms.all()
    
    @property
    def get_remaining_capacity(self):
        """Returns the number of available bed space in this hostel"""
        return (
            (self.rooms.aggregate(models.Sum('capacity'))['capacity__sum']) -
             ( self.rooms.aggregate(models.Sum('book_count'))['book_count__sum'])
        )




class Hostel(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    name = models.CharField(max_length=255)
    hostel_category = models.ForeignKey(HostelCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='hostels', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

    @property
    def get_compound_count(self):
        """Returns the number of compounds in this hostel"""
        return self.compounds.count()
    
    @property
    def get_room_count(self):
        """Returns the number of rooms in this hostel"""
        return self.rooms.count()
    
    @property
    def get_room_capacity_count(self):
        """Returns the number of beds in this hostel"""
        return self.rooms.aggregate(models.Sum('capacity'))['capacity__sum']
    
    @property
    def get_open_rooms(self):
        """Returns the number of rooms in this hostel"""
        return self.rooms.filter(is_active=True).count()
    
    @property
    def get_compounds(self):
        """Returns the number of rooms in this hostel"""
        return self.compounds.all()
    
    @property
    def get_rooms(self):
        """Returns the number of rooms in this hostel"""
        return self.rooms.all()





class Compound(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    name = models.CharField(max_length=255)
    hostel_category = models.ForeignKey(HostelCategory, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='compounds', blank=True, null=True) 
    is_active = models.BooleanField(default=True)
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
        return self.rooms.filter(is_active=True).count()

    def get_rooms(self):
        """Returns the number of rooms in this compound"""
        return self.rooms.all()
    
    @property
    def get_remaining_capacity(self):
        """Returns the number of available bed space in this compound"""
        return (
            (self.rooms.aggregate(models.Sum('capacity'))['capacity__sum']) -
             ( self.rooms.aggregate(models.Sum('book_count'))['book_count__sum'])
        )




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
    hostel = models.ForeignKey(
        HostelCategory, 
        on_delete=models.CASCADE,
        help_text=_("The hostel category this room belongs to"),
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
    image = models.ImageField(upload_to='rooms', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.hostel.name} - { self.compound.name } {self.name}"
    
    @property
    def get_remaining_capacity(self):
        return self.capacity - self.book_count







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
    hostel = models.ForeignKey('client.HostelCategory', on_delete=models.CASCADE)
    compound = models.ForeignKey('client.Compound', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='pending')
    payment_status = models.CharField(max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






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

