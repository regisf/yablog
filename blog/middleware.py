# -*- coding: UTF-8 -*-

""" Network latency smilator """

from django.conf import settings

class AjaxSimulator(object):
    def process_request(self, request):
        if settings.IS_LOCAL:
            import time
            time.sleep(0.5)
            
