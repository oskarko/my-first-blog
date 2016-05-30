from django import template
from django.template.defaulttags import register


@register.filter(name='get_item')
def get_item(dictionary, key):
# Si el nombre se encuentra en el diccionario,
# devuelve la ruta de la imagen de perfil.
    llave = str(key).lower()
    if llave in dictionary:
        return dictionary[llave]
    else:
        return None
