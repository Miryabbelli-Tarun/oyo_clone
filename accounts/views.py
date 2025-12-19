from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import HotelUser
from django.db.models import Q
from django.contrib import messages
from .utils import generateRandomToken
from django.contrib.auth import authenticate,login
# from .utils import sendEmailToken
# Create your views here.

def login_page(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        hotel_user=HotelUser.objects.filter(email=email)
        if not hotel_user.exists():
            messages.warning(request,"Account not found please register first")
            return redirect('login_page')
        if not hotel_user[0].is_verified:
            messages.warning(request,"User email is  not verifyed please verify first")
            return redirect('login_page')
        hotel_user=authenticate(username=hotel_user[0].username,password=password)
        if hotel_user:
            messages.success(request,'Login suceesful')
            login(request,hotel_user)
            return redirect('login_page')
    return render(request,'login.html')

def register(request):
   
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        password=request.POST.get('password')

        hotel_user=HotelUser.objects.filter(Q(email=email) |Q(phone_number=phone_number))
        if hotel_user.exists():
            messages.error(request,"Account with email or phone number already Exist")
            return redirect('register')
        hotel_user=HotelUser.objects.create(
            username=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            email_token=generateRandomToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()
        messages.success(request,"An Email sent to your register email")
        # sendEmailToken(email,hotel_user.email_token)
        return redirect('register')
    return render(request,'register.html')

#A small problem in email sendein we do it manully
#http://127.0.0.1:8000/accounts/verify-account/6c63855f-8400-4f0c-8e36-4a3f7d930a32
def verify_user_account(request,token):
    try:
        hotel_user=HotelUser.objects.get(email_token=token)
        hotel_user.is_verified=True
        hotel_user.save()
        messages.success(request,"Email verifyed")
        return redirect('login_page')
    except Exception:
        return HttpResponse("Invalid token")


    