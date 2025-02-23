from django.shortcuts import render,redirect,HttpResponse
from .models import userdata
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

user_details = settings.MONGO_DB.userdata

# Create your views here.
def index(request):
    return redirect("Login")


def signin(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    if(email and password):
        user = user_details.find_one({ "Email" : email})
        if user:
            if(check_password(password,user["Password"])):
                request.session['email'] = user["Email"]
                return redirect("Dashboard")
            else:
                context = {
                    "message" : "Invalid Password !"
            }
            return render(request,'Login.html',context)
        else:
            context = {
                "message" : "Invalid Email !"
            }
            return render(request,'Login.html',context)
    else:
        return render(request,'Login.html')

def signup(request):
    name = request.POST.get("username")
    email = request.POST.get("usermail")
    password = request.POST.get("userpass")

    if(name and email and password):
        if(user_details.find_one({"Email" : email})):
            context = {
                "message" : "Email Already Exists!"
            }
            return render(request,'Register.html',context)
        else:
            password = make_password(password)
            # userdata.objects.create(name = name, email = email, password = password)
            user_details.insert_one( { "Name" : name, "Email" : email, "Password" : password} )
            return redirect("Login")  
    else:    
        return render(request,'Register.html')
    

def dashboard(request):
    email = request.session.get('email')
    if(email):
        user = user_details.find_one({"Email": email})
        context = {
            "username" : user["Name"]
        }
        return render(request,'dashboard.html',context)
    else:
        return HttpResponse("Please Login")
    


def logout(request):
    request.session.flush()
    return redirect("Login")