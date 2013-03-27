# -*- coding: UTF-8 -*-

from django import template

register = template.Library()

MONTHES = [
    'January',
    'February', 
    'March',
    'April', 
    'May', 
    'June', 
    'July', 
    'August',
    'September', 
    'October', 
    'November', 
    'December' 
]
@register.filter
def month_to_string(value):
    print value
    return MONTHES[int(value)] 