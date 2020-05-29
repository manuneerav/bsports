from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
# Create your views here.

def dashboard(request):
        if request.user.is_authenticated:
                return render(request, 'home/welcome.html')
        else:   
                messages.warning(request,'You first have to login')
                return redirect('/')

def session(request):
        return render(request,'home/dashboard.html')
                
                

