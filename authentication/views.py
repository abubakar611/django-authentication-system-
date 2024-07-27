from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Home view
def home(request):
    return render(request, "authentication/index.html")

# Signup view
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords did not match")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Your account has been successfully created. We have sent you a confirmation email")

        subject = "Welcome to My Platform"
        message = f"Hello {myuser.first_name}!!\nWelcome to My Platform.\nThank you!\nWe have sent you a confirmation email. Please confirm your email to activate your account."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')

    return render(request, "authentication/signup.html",)

# Signin view
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('profile')

        else:
            messages.error(request, "Bad credentials")
            return redirect('signin')

    return render(request, "authentication/signin.html")

# Signout view
def signout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')

# Profile view
@login_required
def profile(request):
    user = request.user

    context = {
        'username': user.username,
        'email': user.email,
        'fname': user.first_name,
        'lname': user.last_name,
    }
    return render(request, "authentication/profile.html", context)
