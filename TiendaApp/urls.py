from django.urls import path

from . import views

urlpatterns = [

    path('',views.tienda, name="Tienda"),

    path('agregar_producto/',views.agregar_producto, name="agregar_producto"),

    path('listar_producto/',views.listar_producto, name="listar_producto"),

    path('modificar_producto/<id>/',views.modificar_producto, name="modificar_producto"),

    path('eliminar_producto/<id>/',views.eliminar_producto, name="eliminar_producto"),

    path('menu_tienda',views.menu_tienda, name="menu_tienda"),



    ################Subastas################3

    path("index", views.index, name="index"),

    

    

    path("register", views.register, name="register"),

    path("new", views.new_listing, name="new_listing"),

    path("listing/<int:listing_id>", views.listing, name="listing"),

    path("new_bid/<int:listing_id>", views.new_bid, name="new_bid"),

    path("close_bid/<int:listing_id>", views.close_bid, name="close_bid"),

    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),

    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),

    path("my_watchlist", views.my_watchlist, name="my_watchlist"),

    path("new_comment/<int:listing_id>", views.new_comment, name="new_comment"),

    path("all_categories", views.all_categories, name="all_categories"),
    
    path("category_branch/<str:category_id>", views.category_branch, name="category_branch"),


    
]

