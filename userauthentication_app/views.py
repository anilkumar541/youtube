from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm

User= settings.AUTH_USER_MODEL



def registerView(request):
    print("kuch nbiidns")

    if request.user.is_authenticated:
        return redirect("coreapp:homepage")

    if request.method== "POST":
        form= UserRegisterForm(request.POST or None)
        if form.is_valid():
            user_data= form.save()
            # email=form.cleaned_data["email"]
            email=form.cleaned_data["username"]
            # password= user_data.cleaned_data("password")
            messages.success(request, f"Hey {email} your account created")
            new_user= authenticate(username= form.cleaned_data["email"], password= form.cleaned_data["password1"])

            login(request, new_user)
            return redirect("coreapp:homepage")


    form= UserRegisterForm()
    context={
        "form":form
    }
    
    return render(request, "signup.html", context)


def loginView(request):
    if request.user.is_authenticated:
        return redirect("coreapp:homepage")
    
    if request.method == "POST":
        email= request.POST.get("email")
        password= request.POST.get("password")

        try:
            user= User.objects.get(email=email)
        except:
            messages.warning(request, "User does not exist")
        
        user= authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in")
            return redirect("coreapp:homepage")
        else:
            messages.warning(request, "Email or password does not exist! try again")

    return render(request, "sign-in.html")


def logoutView(request):
    logout(request)
    return redirect("userauthentication_app:sign-in")

