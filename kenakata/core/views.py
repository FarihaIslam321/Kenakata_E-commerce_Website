from django.http import HttpResponse
from django.shortcuts import render



def home(request):
    return render(request, 'index.html') 

def account(request):
    return render(request, 'account.html') 