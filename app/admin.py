from django.contrib import admin
from app.models import *

# Register your models here.

admin.site.register(myCustomeUser)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Trip)