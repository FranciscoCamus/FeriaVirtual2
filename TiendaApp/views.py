from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from .models import Producto

from .forms import ProductoForm

from AutenticacionApp.models import CustomUser

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def tienda(request):
    if request.user.tipo_usuario in ['comerciante_local', 'productor'] or request.user.is_superuser == True:
        # Si el usuario no es cliente_externo, redirige al login
         # Reemplaza 'nombre_de_tu_url_para_login' con la URL real de tu página de inicio de sesión
        productos = Producto.objects.all()
        return render(request, "TiendaApp/tienda.html", {"productos": productos})
    else: 
        return redirect("login")


@login_required
def agregar_producto(request):
    if request.user.tipo_usuario in ['productor'] or request.user.is_superuser == True:

        data = {
            'form': ProductoForm
        }

        if request.method == 'POST':
            formulario = ProductoForm(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                formulario.save()
                messages.success(request, 'Producto guardado con éxito.')
            else:
                data["form"] = formulario

        return render(request, "TiendaApp/agregar_producto.html", data)
    else: 
        return redirect("login")


def listar_producto(request):

    productos = Producto.objects.all()

    data = {
        'productos' : productos
    }

    return render(request, "TiendaApp/listar_producto.html", data)


def modificar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)

    data = {
        'form' : ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files= request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Producto modificado con éxito.')
            return redirect(to='listar_producto')
        data['form'] = formulario

    return render(request, "TiendaApp/modificar_producto.html", data)

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, 'producto eliminado con éxito.')
    return redirect(to="listar_producto")



def menu_tienda(request):

    return render(request, "TiendaApp/menu_tienda.html")





##############################Subastas#################################3

#CS50 Commerce Project 2021- Author: Luis Balladares
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from .models import CustomUser, Auction_listing, Bids, Comments
from . import forms
from django.template.defaulttags import register
from django.contrib import messages



@register.filter
def get_bid(dictionary, key):
    return dictionary.get(key)

def index(request):
    active_listings = Auction_listing.objects.filter(active_status=True).all()
    id_and_bid = {}

    for listing in active_listings:
        current_bid = Bids.objects.filter(pk=listing.id).first()
        bid_amount = current_bid.highest_bid if current_bid else 0
        id_and_bid[int(listing.id)] = bid_amount

    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "id_and_bid": id_and_bid
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")



from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'registration/register_success.html', {'username': username})
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


from .forms import listingform,bidform
from django.conf import settings
import os

from django.shortcuts import render, redirect
from django.contrib import messages

import os
from django.conf import settings

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import listingform  # Asegúrate de importar tu formulario

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import listingform
from .models import Bids
import os
from django.conf import settings

@login_required(login_url='auctions/login.html')
def new_listing(request):
    if request.method == "POST":
        form = listingform(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user

            # Verifica si no se ha proporcionado una imagen y asigna la imagen predeterminada
            if not listing.img_url:
                listing.img_url = 'tienda/subastasdefault.jpg'  # Asegúrate de tener la imagen por defecto en la carpeta 'tienda'

            listing.save()

            # Crear una nueva oferta (Bids) para la nueva subasta
            current_bid = Bids(listing=listing, highest_bid=listing.starting_bid, highest_bid_user=request.user)
            current_bid.save()

            messages.success(request, "La subasta ha sido creada exitosamente!!")
            return redirect("index")
    else:
        form = listingform()

    return render(request, "auctions/new_listing.html", {"form": form})




# Resto del archivo de vistas sigue igual...

@login_required
def listing(request, listing_id):
    if request.user.tipo_usuario == 'cliente_externo' or request.user.is_superuser == True:
        listing = Auction_listing.objects.get(pk=listing_id)
        current_bid = Bids.objects.get(pk=listing.id)
        category = listing.get_category_display()
        comments_list = Comments.objects.filter(listing_id=listing_id)

        if listing.watchlist.filter(id=request.user.id):
            usertocheck = True
        else:
            usertocheck = False

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "current_bid": current_bid,
            "bidform": forms.bidform(),
            "usertocheck": usertocheck,
            "category": category,
            "comment": forms.commentform(),
            "comments_list": comments_list
        })
    else: 
        return redirect("login")

@login_required(login_url='auctions/login.html')
def new_bid(request, listing_id):
    if request.method == 'POST':
        form = forms.bidform(request.POST)
        if form.is_valid():            
            listing = Auction_listing.objects.get(pk=listing_id)
            current_bid = Bids.objects.get(pk=listing_id)
            category = listing.get_category_display()
            comments_list = Comments.objects.filter(listing_id=listing_id)

            if listing.watchlist.filter(username=request.user):
                usertocheck = True
            else:
                usertocheck = False

            bid_to_place = form.save(commit=False)

            if bid_to_place.highest_bid > current_bid.highest_bid:
                bid_to_place.highest_bid_user = request.user  # Esto debería ser una instancia de CustomUser
                bid_to_place.listing = listing
                bid_to_place.save()
                messages.success(request, "Tu oferta fué publicada con Exito!")

                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "current_bid": bid_to_place,
                    "usertocheck": usertocheck,
                    "bidform": forms.bidform(),
                    "category": category,
                    "comment": forms.commentform(),
                    "comments_list": comments_list
                })
            elif bid_to_place.highest_bid == current_bid.highest_bid:
                if listing.author == current_bid.highest_bid_user:
                    bid_to_place.highest_bid_user = str(request.user)
                    bid_to_place.id = listing
                    bid_to_place.save()
                    messages.success(request, "Your bid was successfully placed!")
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "current_bid": bid_to_place,
                        "bidform": forms.bidform(),
                        "usertocheck": usertocheck,
                        "category": category,
                        "comment": forms.commentform(),
                        "comments_list": comments_list
                    })
                else:
                    messages.error(request, "Your bid must be higher than the current price!")
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "current_bid": bid_to_place,
                        "bidform": forms.bidform(),
                        "usertocheck": usertocheck,
                        "category": category,
                        "comment": forms.commentform(),
                        "comments_list": comments_list
                    })
            else:
                messages.error(request, "Tu oferta no puede ser menor a la que ya existe!")
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "usertocheck": usertocheck,
                    "category": category,
                    "comment": forms.commentform(),
                    "comments_list": comments_list
                })
        else:
            active_listings = Auction_listing.objects.filter(active_status=True).all()
            id_and_bid = {}
            for listing in active_listings:
                current_bid = Bids.objects.get(pk=listing.id)
                id_and_bid[int(listing.id)] = current_bid.highest_bid

            return render(request, "auctions/index.html", {
                "active_listings": active_listings,
                "id_and_bid": id_and_bid
            })
    else:
        active_listings = Auction_listing.objects.filter(active_status=True).all()
        id_and_bid = {}
        for listing in active_listings:
            current_bid = Bids.objects.get(pk=listing.id)
            id_and_bid[int(listing.id)] = current_bid.highest_bid

        return render(request, "auctions/index.html", {
            "active_listings": active_listings,
            "id_and_bid": id_and_bid
        })




from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Auction_listing, Bids, Comments
from .forms import bidform, commentform

from django.shortcuts import render, get_object_or_404, redirect

@login_required
def close_bid(request, listing_id):
    listing = get_object_or_404(Auction_listing, pk=listing_id)
    
    if request.method == 'POST':
        current_bid = Bids.objects.get(listing=listing)

        # Verificar si el usuario actual es el autor de la subasta
        if request.user == listing.author:
            listing.active_status = False
            listing.save()

            category = listing.get_category_display()
            comments_list = Comments.objects.filter(listing_id=listing_id)

            if current_bid.highest_bid_user:
                winner_user = CustomUser.objects.get(username=current_bid.highest_bid_user)
                messages.success(request, f"¡Cerraste esta subasta! Ponte en contacto con el ganador, usuario: {winner_user.username}")
            else:
                messages.error(request, "Cerró esta subasta sin postores. ¡Te deseamos éxito la próxima oportunidad!")

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "current_bid": current_bid,
                "bidform": bidform(),
                "category": category,
                "comments_list": comments_list,
                "comment": commentform(),
            })

        else:
            messages.error(request, "You are not authorized to close this auction.")
            return redirect("listing", listing_id=listing_id)
    else:
        current_bid = Bids.objects.get(listing=listing)
        category = listing.get_category_display()
        comments_list = Comments.objects.filter(listing_id=listing_id)

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "current_bid": current_bid,
            "bidform": bidform(),
            "comments_list": comments_list,
            "comment": commentform(),
            "category": category,
        })




@login_required(login_url='auctions/login.html')
def add_watchlist(request, listing_id):
    current_bid = Bids.objects.get(pk=listing_id)
    listing = Auction_listing.objects.get(pk=listing_id)
    category = listing.get_category_display()
    comments_list = Comments.objects.filter(listing_id=listing_id)

    usertowatchlist = CustomUser.objects.get(username=request.user)
    listing.watchlist.add(usertowatchlist)

    try:
        listing.save()
    except IntegrityError:
        messages.error(request, "There was an error trying to process your request, please try again.")
        usertocheck = False

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "current_bid": current_bid,
            "bidform": forms.bidform(),
            "usertocheck": usertocheck,
            "comments_list": comments_list,
            "comment": forms.commentform(),
            "category": category
        })

    messages.success(request, "La subasta fué agregada correctamente a tu lista de subastas")
    usertocheck = True

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_bid": current_bid,
        "bidform": forms.bidform(),
        "usertocheck": usertocheck,
        "comments_list": comments_list,
        "comment": forms.commentform(),
        "category": category
    })


@login_required(login_url='auctions/login.html')
def remove_watchlist(request, listing_id):
    current_bid = Bids.objects.get(pk=listing_id)
    listing = Auction_listing.objects.get(pk=listing_id)
    category = listing.get_category_display()
    comments_list = Comments.objects.filter(listing_id=listing_id)

    usertoremove = CustomUser.objects.get(username=request.user)
    listing.watchlist.remove(usertoremove)

    try:
        listing.save()
    except IntegrityError:
        messages.error(request, "There was an error trying to process your request, please try again.")
        usertocheck = True

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "current_bid": current_bid,
            "bidform": forms.bidform(),
            "usertocheck": usertocheck,
            "comments_list": comments_list,
            "comment": forms.commentform(),
            "category": category
        })

    messages.success(request, "Eliminaste exitosamente la subasta de tu lista!")
    usertocheck = False

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_bid": current_bid,
        "bidform": forms.bidform(),
        "usertocheck": usertocheck,
        "comments_list": comments_list,
        "comment": forms.commentform(),
        "category": category
    })



from django.db import IntegrityError


@login_required(login_url='auctions/login.html')
def my_watchlist(request):
    myuser = CustomUser.objects.get(username=request.user)
    userwatchlist = myuser.user_watchlist.all()
    id_and_bid = {}

    for listing in userwatchlist:
        current_bid = Bids.objects.get(pk=listing.id)
        id_and_bid[int(listing.id)] = current_bid.highest_bid

    return render(request, "auctions/watchlist.html", {
        "userwatchlist": userwatchlist,
        "id_and_bid": id_and_bid
    })

@login_required(login_url='auctions/login.html')
def new_comment(request, listing_id):
    if request.method == 'POST':
        listing = Auction_listing.objects.get(pk=listing_id)
        current_bid = Bids.objects.get(pk=listing_id)
        form = forms.commentform(request.POST)
        category = listing.get_category_display()

        if form.is_valid():
            newcomment = form.save(commit=False)
            newcomment.listing_id = listing
            newcomment.post_author = request.user  # Cambio aquí

            if listing.watchlist.filter(username=request.user):
                usertocheck = True
            else:
                usertocheck = False

            try:
                newcomment.save()
            except IntegrityError:
                messages.error(request, "There was an error trying to process your request, please try again.")
                comments_list = Comments.objects.filter(listing_id=listing_id)
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "usertocheck": usertocheck,
                    "comments_list": comments_list,
                    "comment": forms.commentform(),
                    "category": category
                })

            messages.success(request, "Comentario publicado con éxito!!")
            comments_list = Comments.objects.filter(listing_id=listing_id)
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "current_bid": current_bid,
                "bidform": forms.bidform(),
                "comments_list": comments_list,
                "usertocheck": usertocheck,
                "comment": forms.commentform(),
                "category": category
            })
        else:
            comments_list = Comments.objects.filter(listing_id=listing_id)
            if listing.watchlist.filter(username=request.user):
                usertocheck = True
            else:
                usertocheck = False
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "current_bid": current_bid,
                    "bidform": forms.bidform(),
                    "comments_list": comments_list,
                    "usertocheck": usertocheck,
                    "comment": forms.commentform(),
                    "category": category
                })

    else:
        category = listing.get_category_display()
        comments_list = Comments.objects.filter(listing_id=listing_id)

        if listing.watchlist.filter(username=request.user):
            usertocheck = True
        else:
            usertocheck = False

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "current_bid": current_bid,
            "bidform": forms.bidform(),
            "usertocheck": usertocheck,
            "category": category,
            "comments_list": comments_list,
            "comment": forms.commentform()
        })



def all_categories(request):
    return render(request, "auctions/all_categories.html")

def category_branch(request, category_id):
    categorylist = Auction_listing.objects.filter(active_status=True, category=category_id)
    if categorylist:
        aux = categorylist.first()
        categorytitle = aux.get_category_display()

        id_and_bid = {}
        for listing in categorylist:
            current_bid = Bids.objects.get(pk=listing.id)
            id_and_bid[int(listing.id)] = current_bid.highest_bid

        return render(request, "auctions/category_branch.html", {
            "categorylist": categorylist,
            "id_and_bid": id_and_bid,
            "categorytitle": categorytitle
        })

    else:
        return render(request, "auctions/category_branch.html", {
            "categorylist": False
        })


