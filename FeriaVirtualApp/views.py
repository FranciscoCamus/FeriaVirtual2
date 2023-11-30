from django.shortcuts import render, HttpResponse

from CarroApp.carro import Carro

# Create your views here.

def home(request):

    carro = Carro(request)

    return render(request, "FeriaVirtualApp/home.html")





def blog(request):

    return render(request, "FeriaVirtualApp/blog.html")

def contacto(request):

    return render(request, "FeriaVirtualApp/contacto.html")