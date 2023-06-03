from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("¡Hola, mundo!")

def login(request):
    return render(request, 'login.html')

def contact(request):
    return render(request, 'contact.html')