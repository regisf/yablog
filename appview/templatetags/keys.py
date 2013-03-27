# -*- coding: UTF-8 -*-

from django import template

register = template.Library()

@register.filter
def keys(value, arg):
    return value[arg]