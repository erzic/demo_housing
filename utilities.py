def limpiar_precios(precio):
    precio = str(precio).split(" ")[0].replace("$", "").replace(",", "")

    return precio

def limpiar_m2(m2):
    return m2.replace(" m2", "")

def limpiar_location(location):
    return location.replace("\n ", "")