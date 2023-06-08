from django.contrib import admin

from .models import HostelCategory, Compound, Room, Hostel, Booking, Document



class HostelInline(admin.StackedInline):
    model = Hostel
    extra = 2

class HostelCategoryAdmin(admin.ModelAdmin):
    inlines = [HostelInline]


class RoomInline(admin.StackedInline):
    model = Room
    extra = 2

class CompoundAdmin(admin.ModelAdmin):
    inlines = [RoomInline]


class CompoundInline(admin.StackedInline):
    model = Compound
    extra = 2

class HostelAdmin(admin.ModelAdmin):
    inlines = [CompoundInline]


admin.site.register(HostelCategory,HostelCategoryAdmin)
admin.site.register(Compound, CompoundAdmin)
admin.site.register(Room)
admin.site.register(Hostel, HostelAdmin)
admin.site.register(Booking)
admin.site.register(Document)
