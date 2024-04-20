from django.urls import path
from .views import create_ticket,booking

urlpatterns = [
    path("create_ticket/",create_ticket,name="create_ticket"),
    path("booking/",booking,name="booking")    
]
