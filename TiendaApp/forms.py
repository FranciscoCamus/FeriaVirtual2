from django import forms

from .models import Producto

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'



##########Subastas###########################


#CS50 Commerce Project 2021- Author: Luis Balladares
from django.forms import ModelForm
from .models import Auction_listing, Bids, Comments

class listingform(ModelForm):
    class Meta:
        model = Auction_listing
        fields = ['title', 'description', 'starting_bid', 'img_url', 'category']
        labels = {
            'title': 'Titulo',
            'description': 'Descripción',
            'starting_bid': 'Tu oferta inicial',
            'img_url': 'Carga tu imagen(opcional)',
            'category': 'Categoría'
        }

class bidform(ModelForm):
    class Meta:
        model = Bids
        fields = ['highest_bid']
        labels = {'highest_bid': ''}

class commentform(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        labels = {'comment': ''}
