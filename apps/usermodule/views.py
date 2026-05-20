from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered! Please login.') 
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def protected_view(request):
    return HttpResponse("<h2>This is a protected page. You are logged in!</h2><br><a href='/users/logout/'>Logout</a>")

def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out.') 
    return redirect('login')