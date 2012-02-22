# -*- coding; UTF-8 -*-

from django.template import loader, Context
from django.http import HttpResponse

from notification import notification_send

def index(req):
    try:
        context = Context()
        context['test'] = "Hello world"
        notification_send('confirm', 'YOUR-EMAIL-HERE@YOUR-DOMAIN-NAME.HERE', context=context)
        return HttpResponse("OK")
    except Exception, e:
        return HttpResponse("Fail : %s" % e)
