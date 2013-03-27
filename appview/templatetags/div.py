# -*- coding: UTF-8 -*-

from django import template

register = template.Library()

@register.filter
def div(count, divider):
    divider = float(divider)
    if divider == 0.0:
        return 'Division per 0'
    
    return "%.2f" % ((count / divider) * 100)

@register.filter
def mul(value, multiple):
    return int(float(value) * int(multiple))