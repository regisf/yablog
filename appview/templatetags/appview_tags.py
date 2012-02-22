# -*- coding: UTF-8 -*-

from django import template

from appview.models import View

register = template.Library()

class AppViewArgumentMissing(Exception):
    pass

class AppViewWrongAction(Exception):
    pass


@register.tag
def appview_get_view_count_for(p,t):
    args = t.split_contents()
    if len(args) != 4:
        raise AppViewArgumentMissing()
        
    name, origin, action, context_var = args
    
    if action != "as":
        raise AppViewWrongAction()
        
    class AppViewInit(template.Node):
        def render(self, context):
            url = template.Variable(origin).resolve(context)
            context[context_var] = View.objects.filter(internal_url=url).count()
            return ''
    return AppViewInit()