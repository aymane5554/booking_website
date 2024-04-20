"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("main.urls")),
    path("register",views.register,name="register"),
    path("login",views.login_view,name="login"),
    path("",views.index,name="index"),
    path("Profile/<str:username>",views.profile,name="profile"),
    path("logout",views.logout_view,name="logout"),
    path("event/<int:id>",views.event_page,name="event_page"),  
    path("new_event/",views.create_event_view,name="create_event"),  
    path("result",views.result,name="result")
]
