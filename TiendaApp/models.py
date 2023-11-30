from django.db import models

# Create your models here.


class CategoriaProd(models.Model):
    nombre= models.CharField(max_length=50)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "CategoriaProd"
        verbose_name_plural = "CategoriasProd"

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    categorias = models.ForeignKey(CategoriaProd, on_delete= models.CASCADE)
    imagen = models.ImageField(upload_to="tienda", null=True, blank=True)
    precio = models.FloatField()
    disponibilidad = models.BooleanField(default=True)
    created = models.DateField(auto_now_add = True)
    updated = models.DateField(auto_now = True)

    class Meta: 
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


####################Subastas#####################

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Auction_listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=timezone.now())
    
    # Cambia el autor al nuevo modelo de usuario personalizado
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    img_url = models.ImageField(upload_to='tienda', blank=True, null=True)
    watchlist = models.ManyToManyField(CustomUser, blank=True, related_name="user_watchlist")
    active_status = models.BooleanField(default=True)

    categories_list = (
        ('UV', 'Uvas'),
        ('PL', 'Platanos'),
        ('FR', 'Frutillas'),
        ('NA', 'Naranjas'),
        ('CE', 'Cerezas'),
        ('MA', 'Mandarinas'),
        ('FB', 'Frambuesas'),
        ('PI', 'Piñas'),
        ('OT', 'Otros')
        
    )
   
    category = models.CharField(max_length=2, choices=categories_list, default='OT', help_text="Si no se especifica se auto asigna como otros")    

    def save(self, *args, **kwargs):
        if not self.img_url:  # Si no se proporciona una imagen, establece una imagen por defecto
            self.img_url = 'tienda/subastasdefault.jpg'  # Cambia 'default.jpg' por tu imagen por defecto
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-creation_date',)

    def __str__(self):
        return f"{self.id} {self.title} -- {self.creation_date}"

class Bids(models.Model):
    # Cambia a ForeignKey para enlazar con AuctionListing
    listing = models.OneToOneField(Auction_listing, on_delete=models.CASCADE, primary_key=True, related_name="listing_bid")
    
    highest_bid = models.IntegerField(default=0)
    
    # Cambia el usuario al nuevo modelo de usuario personalizado
    highest_bid_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    last_bid_date = models.DateTimeField(auto_now=timezone.now())

    class Meta:
        ordering = ('last_bid_date',)

    def __str__(self):
        return f"-- Bid $ {self.highest_bid} by {self.highest_bid_user.username} on -- {self.last_bid_date}"

class Comments(models.Model):
    listing_id = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="listing_comments")
    
    # Cambia el autor al nuevo modelo de usuario personalizado
    post_author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    commentary_date = models.DateTimeField(auto_now_add=timezone.now()) 
    comment = models.TextField(null=True)

    def __str__(self):
        return f"Listing id: {self.listing_id} by {self.post_author.username} on {self.commentary_date}"

