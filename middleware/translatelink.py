# -*- coding: UTF-8 -*-

""" Network latency smilator """

import re

from django.conf import settings

class AjaxSimulator(object):
    def process_request(self, request):
        if settings.IS_LOCAL:
            import time
            time.sleep(0.5)
            

class TranslateLinkModifier(object):
    """ This middleware add on each link found on a page a query key to be sure that the
    selected language continue to be selected
    """
    def process_response(self, request, response):
        if 'text/html' in response['content-type']:
            if request.session.has_key('lang'):
                lang = request.session['lang'].strip()
                response.content = re.sub(r'href="(.*?)"', 'href="\\1?lang={0}"'.format(lang), response.content)
                response.content = re.sub(r'href="(.*?)\?lang=(\w{2})\?lang=%s"' % lang, 'href="\\1?lang=\\2"', response.content)
                del request.session['lang']
        
        return response
    
