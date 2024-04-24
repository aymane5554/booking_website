from django.urls import path
from .views import booking

urlpatterns = [
    path("booking/",booking,name="booking")    
]
