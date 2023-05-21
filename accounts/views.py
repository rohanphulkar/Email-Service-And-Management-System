from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
import random
from .helper import send_otp
from utils.username_suffix_check import check_suffix

# User Registration View
def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=="POST":
        # Retrieve form data from the request
        name = request.POST.get("name")
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")


        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return render(request, "accounts/register.html")
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "accounts/register.html")
        
        # Split the username and remove the domain if present
        if len(username.split("@"))>1:
            username = username.split("@")[0]

        # Create a new user
        user = User.objects.create(
            username=username,
            name = name,
            phone = phone,
            gender = gender,
        )
        user.set_password(password)
        user.save()
        return redirect("login")
    return render(request, "accounts/register.html")


# User login view
def signin(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=="POST":

        # Retrieve login credentials
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Append domain if missing from the username
        username = check_suffix(username)
        
        #  Retrieve the user
        user = User.objects.filter(username=username)

        # Check if user exists
        if not user.exists():
            messages.error(request, "User not found")
            return render(request,"accounts/login.html")
        
        # Check the password
        user_password = user.first().password
        if not check_password(password, user_password):
            messages.error(request, "Wrong password")
            return render(request,"accounts/login.html")
        
        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            return redirect("home")
        messages.error(request,"Login failed")
    return render(request, "accounts/login.html")

# View for checking username availability
def check_username(request, username):
    username = f"{username}@metabyte.one"
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

# Logout view
@login_required(login_url="/accounts/login/")
def Logout(request):
    logout(request)
    return redirect("login")

# Forgot password view
def forgot_password(request):
    if request.method=="POST":
        username = request.POST.get("username")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return render(request,"accounts/forgot_password.html")
        
        verification_code = random.randint(0000,9999)
        user.pwd_reset_code = verification_code
        user.save()

        message = send_otp(user.phone, verification_code)
        if message:
            messages.success(request,"A verification code has been sent to your phone.")
        else:
            messages.error(request, "Something went wrong")
        return redirect("reset_password",user.id)
    
    return render(request,"accounts/forgot_password.html")


# Reset password view
def reset_password(request,id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return redirect("forgot_password")
    
    if request.method=="POST":
        code = request.POST.get("code")
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if user.pwd_reset_code != code:
            messages.error(request, "Verification code is incorrect.")
            return redirect("reset_password",id)
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password",id)
        
        user.set_password(new_password)
        user.pwd_reset_code = ""
        user.save()
        messages.success(request,"Your password has been changed.")
        return redirect("login")
    
    return render(request,"accounts/reset_password.html")

# User settings view
def user_settings(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method=="POST":
            full_name = request.POST.get("full-name")
            phone = request.POST.get("phone")
            gender = request.POST.get("gender")
            current_password = request.POST.get("current-password")
            new_password = request.POST.get("new-password")

            if full_name:
                user.name = full_name
            if phone:
                user.phone = phone
            if gender:
                user.gender = gender

            # check if passwords are provided and are equal and valid
            if current_password and new_password and check_password(current_password, user.password):
                # change the password 
                user.set_password(new_password)
            user.save()
        return render(request,"accounts/settings.html")
    return redirect("login")