from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class UserAdmin(UserAdmin):
    pass
admin.site.register(User, UserAdmin)
admin.site.register(JobListing)
admin.site.register(Saved)
admin.site.register(History)
admin.site.register(Lists)
admin.site.register(CustomListings)