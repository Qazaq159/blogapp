from django.shortcuts import render
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)

                response = Response({"message": "Registration successful", "token": token.key},
                                    status=status.HTTP_201_CREATED)
                response.set_cookie(
                    key='auth_token',
                    value=token.key,
                    httponly=True,
                    secure=False,
                    samesite='Lax'
                )
                return response
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid credentials.")

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Save the user form and create the user
            user = user_form.save()

            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            response = Response({"message": "Registration successful", "token": token.key},
                                status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='auth_token',
                value=token.key,
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            return response
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserRegistrationForm()

    return render(request, 'register.html', {'user_form': user_form})
