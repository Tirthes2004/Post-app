from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from .models import PendingSignup
from .forms import SignUpForm, OTPForm
from django.contrib import messages, auth
from django.conf import settings

# Create your views here.

# accounts/views.py
def user_register(request):
    step = 'signup'
    form = SignUpForm()

    if request.method == 'POST':
        if request.session.get('pending_email'):
            # OTP Verification Step
            step = 'verify'
            email = request.session.get('pending_email')
            otp_input = request.POST.get('otp')

            pending = PendingSignup.objects.filter(email=email).first()
            if pending and otp_input == pending.otp:
                # OTP correct — create user
                User.objects.create_user(
                    username=pending.username,
                    email=pending.email,
                    password=pending.password
                )
                pending.delete()
                del request.session['pending_email']
                return redirect('login')  # replace 'login' with your login URL name

            else:
                # Wrong OTP
                return render(request, 'register.html', {
                    'step': 'verify',
                    'form': OTPForm(),  # ⬅️ This is the missing piece!
                    'error': 'Invalid OTP. Please try again.'
                })

        else:
            # Registration Form Step
            form = SignUpForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                # Generate and email OTP
                otp = str(random.randint(100000, 999999))
                send_mail(
                    subject='Your OTP Code',
                    message=f'Your OTP is {otp}',
                    from_email='tirthessamanta03@gmail.com',
                    recipient_list=[email],
                )

                # Save temporary signup
                PendingSignup.objects.filter(email=email).delete()  # remove duplicates
                PendingSignup.objects.create(username=username, email=email, password=password, otp=otp)
                request.session['pending_email'] = email

                return render(request, 'register.html', {'step': 'verify', 'form': OTPForm()})


    return render(request, 'register.html', {'form': form, 'step': step})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('tweet_list')  # or homepage
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('tweet_list')  # or homepage
