from django.contrib import admin
from .models import Event,Ticket,Bookings,User,Rank
# Register your models here.

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Bookings)
admin.site.register(User)
admin.site.register(Rank)