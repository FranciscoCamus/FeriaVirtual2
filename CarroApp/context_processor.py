def importe_total_carro(request):
    total = 0

    if request.user.is_authenticated:
        for key, value in request.session["carro"].items():
            precio_str = str(value["precio"]).replace(',', '.')
            total += float(precio_str)
    else:
        total = "Debes hacer login"

    return {"importe_total_carro":total}