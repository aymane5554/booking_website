from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Event(models.Model):
    title = models.CharField(max_length = 128)
    description = models.TextField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField()
    type = models.CharField(max_length=32)
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name="events")
    selling = models.BooleanField(default=False)

    def serializer(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'address' : self.address,
            'created_at' : self.created_at,
            'start_at' : self.start_at,
            'type' : self.type,
            'capacity' : self.capacity,
            'user' : self.user.id
        }

    def __str__(self) -> str:
        return self.title

class Ticket(models.Model):
    type = models.CharField(max_length=24)
    price = models.IntegerField()
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="tickets")
    number = models.IntegerField(default=0)

    def serializer(self):
        return {
            'type' : self.type,
            'price' : self.price,
            'event' : self.event.id 
        }

class Bookings(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="ticket_bookings")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_bookings")
    password = models.CharField(max_length=20)
    is_used = models.BooleanField(default=False)

    def serializer(self):
        return {
            'id' : self.id,
            'ticket' : self.ticket.id,
            'user' : self.user.id
        }

class Rank(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_rankings")
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="event_rankings")
    score = models.IntegerField(default=0)
    cmnt = models.CharField(max_length=128)