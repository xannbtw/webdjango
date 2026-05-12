def cantidad_carrito(request):
    total = 0
    if 'carrito' in request.session: # si ya hay un carrito
        for key, value in request.session['carrito'].items():
            total += value['cantidad'] # suma la cantidad de cada prod guardado
            
    return {'cantidad_carrito' : total} #envia la cantidad al html