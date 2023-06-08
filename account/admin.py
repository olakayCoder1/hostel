from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User 
# Register your models here.

class PreferenceModelAdmin(admin.ModelAdmin):
    list_display = ['name']





class UserAdmin(UserAdmin):
    ordering= ('-created_at',) 
    list_filter = ['first_name','email', 'gender']
    list_display = ['email','is_active','is_staff'] 
    search_fields =  ('first_name','email')
    fieldsets = (
        (None, { 'fields': ('email', 'first_name', 'last_name','gender')}),
        ('Permissions',{'fields':('is_staff','is_active','is_superuser','groups',"user_permissions")}),
    )
    add_fieldsets = (
        (None, {     
            'classes': ('wide',),
            'fields': ('email' , 'first_name', 'last_name',  'password1', 'password2'),}),)
    

admin.site.register(User, UserAdmin)