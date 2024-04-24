from django.http import HttpResponseRedirect,JsonResponse, HttpResponse
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login, logout
from .models import Event,Ticket,Bookings,User,Rank
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json,datetime,string,random

# Create your views here.

def index(request,):
    return render(request,"index.html",{"events":Event.objects.all().order_by("-created_at")})

def result(request):
    s = request.GET["s"]
    events = Event.objects.filter(title__contains=s) 
    users = User.objects.filter(username__contains=s) 
    return render(request,"result.html",{"events":events , "users":users})

def profile(request,username):
    user = User.objects.get(username=username)
    es = user.events.all()
    rsums = 0
    rs = len(es)
    for e in es :
        for r in e.event_rankings.all():
            rsums += r.score
    rate = 0
    if rsums ==0 or rs == 0 : 
        rate = 0
    else: 
        rate = rsums/rs
    return render(request,"profile.html",{"rate":rate,"user" : user, "bookings" : user.user_bookings.all().order_by("-id"),"events" :user.events.all().order_by("-created_at")})

def ticket_valid(type,price,number):
    if len(type.strip()) > 0 and int(price) >0 and int(number) > 0 :
        return True
    return False

@csrf_exempt
def event_page(request,id):
    event = Event.objects.get(pk=id)
    current_date = datetime.datetime.now()
    current_date = current_date.replace(tzinfo=datetime.timezone.utc)
    sold = 0
    capacity = 0
    for ticket in event.tickets.all():
        capacity += ticket.number
    for ticket in event.tickets.all():
        sold += len(ticket.ticket_bookings.all())
    if sold != 0 :
        percentage = (sold/capacity)*100
    else : 
        percentage = 0
    if current_date >= event.start_at:
        if request.user.is_authenticated:
            if request.method == "POST":
                score = request.POST["stars"]
                cmnt = request.POST["rate"]
                Rank.objects.create(user=request.user,event=event,score=int(score),cmnt=cmnt)
                return redirect(f"/event/{id}")
            tl = Ticket.objects.filter(event=event)
            bk = request.user.user_bookings.all()
            can_rate = False
            for b in bk :
                if b.ticket in tl :
                    can_rate = True
            sum_of_rates = 0
            rated = False

            for r in event.event_rankings.all():
                sum_of_rates += r.score

            number_of_rates = len(event.event_rankings.all())
            event_rate = 0
            if sum_of_rates== 0 or number_of_rates==0:
                event_rate = 0
            else:
                event_rate = sum_of_rates/number_of_rates 

            if len(event.event_rankings.filter(user=request.user)) > 0:
                rated = True
                can_rate = False
                return render(request,"fevent.html",{"review":Rank.objects.get(user = request.user,event=event),"rated":rated,"event":event,"tickets_sold" : sold , "percentage" : percentage,"capacity" :capacity,"can_rate":can_rate,"event_rate":event_rate,"number_of_rates":number_of_rates})
            return render(request,"fevent.html",{"rated":rated,"event":event,"tickets_sold" : sold , "percentage" : percentage,"capacity" :capacity,"can_rate":can_rate,"event_rate":event_rate,"number_of_rates":number_of_rates})
    if request.method == "POST" :
        title = request.POST["type"]
        price =request.POST["price"]
        number = request.POST["tickets"]
        if request.user != event.user : 
            return render(request,"event.html",{"msg":"false informations","event":event ,"tickets_available":capacity-sold,"tickets_sold" : sold , "percentage" : percentage,"capacity" :capacity})
        if ticket_valid(type=title,price=price,number=number):
            Ticket.objects.create(type=title,price=price,event=event,number=number)
            return redirect(f"/event/{id}")
        return render(request,"event.html",{"msg":"false informations","event":event ,"tickets_available":capacity-sold,"tickets_sold" : sold , "percentage" : percentage,"capacity" :capacity})
    return render(request,"event.html",{"event":event ,"tickets_available":capacity-sold,"tickets_sold" : sold , "percentage" : percentage,"capacity" :capacity})

def is_event_valid(title,description,address,type):
        if len(title.strip()) > 0  and len(description.strip()) > 0 and len(address.strip()) > 0 and len(type.strip()) > 0:
            return True
        return False

@csrf_exempt
@login_required(login_url="/login")
def create_event_view(request):
    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["description"]
        location  =request.POST["address"]
        datetime = request.POST["start-at"]
        tpe = request.POST["type"] 
        user = request.user
        if is_event_valid(title=title,description=desc,address=location,type=tpe):
            Event.objects.create(title=title,description=desc,address=location,start_at=datetime,type=tpe,user=user) 
            id = Event.objects.get(title=title,description=desc,address=location,start_at=datetime,type=tpe,user=user) .id
            return redirect(f"/event/{id}")
        return render(request,"create_event.html",{"msg" : "Something is wrong !!!"})
    return render(request,"create_event.html")

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated :
        return HttpResponseRedirect(reverse("index"))
    
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def register(request):
    if request.user.is_authenticated :
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password1"]
        confirmation = request.POST["password2"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
    
def password():
    chars = ""
    chars += string.ascii_letters
    chars += string.digits
    chars+= string.punctuation.replace(',', '')
    p = ""
    for i in range(20):
        p+=random.choice(chars)
    return p

@login_required(login_url="/login")
@csrf_exempt
def booking(request):
    sold = 0
    capacity = 0
    percentage = 0
    if request.method == "POST":
        data = json.loads(request.body)
        ticket = Ticket.objects.get(pk=int(data.get("id")))
        tsold = len(ticket.ticket_bookings.all())
        if ticket.number-tsold <= 0 :
             return JsonResponse({"msg" : "tickets already sold out"})
        Bookings.objects.create(ticket=ticket,user=request.user,password=password())
        event = ticket.event
        for ticket in event.tickets.all():
            capacity += ticket.number
        for ticket in event.tickets.all():
            sold += len(ticket.ticket_bookings.all())
        if sold != 0 :
            percentage = (sold/capacity)*100
        else : 
            percentage = 0
        return JsonResponse({"msg" : "ticket bought. go to your profile to see it","percentage":percentage,"capacity":capacity,"sold":sold})
    return JsonResponse({"error" : "post method required"})

@login_required(login_url="/login")
def check(request):
    book = Bookings.objects.get(pk =int(request.GET["i"])) 
    p = request.GET["p"]
    if  request.user.id == book.ticket.event.user.id:
        if book.is_used == False and book.password ==p :
            book.is_used = True
            book.save()
            return render(request,"validation.html",{"valid":True})
        return render(request,"validation.html",{"valid":False})
    return render(request,"validation.html",{"valid":True}) if book.is_used == False else render(request,"validation.html",{"valid":False})