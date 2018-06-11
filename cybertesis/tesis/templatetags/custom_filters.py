# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name='no_star_range')
def no_star_range(val1, val2):
    """ Retorna una lista iterable de NO estrellas """
    try:
        a = int(val1)
        b = int(val2)
        return ['x' for c in range(a - b)]
    except:
        return 0


@register.filter(name='star_range')
def star_range(val):
    """ Retorna lista iterable que representa la cantidad de estrellas de la valoración """
    five_stars = ['*', '*', '*', '*', '*']
    return five_stars[:val]


@register.filter(name='translate')
def translate(val):
    dictionary = {'T': 'Tesis', 'MS': 'Maestría', 'TMS': 'Tesis Maestría', 'TD': 'Tesis Doctoral'}
    if val == '':
        return ''
    elif val in dictionary:
        return dictionary[val]
    return ''
