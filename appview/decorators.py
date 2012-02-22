# -*- coding: UTF-8 -*-

"""
AppView
"""

import datetime
from appview.models import Exclude, View
from notification import ajax_log

def is_new(request):
    meta = request.META
    for ex in Exclude.objects.all():        
        if ex.exclude_IP == meta.get('REMOTE_ADDR') or  ex.match(meta.get('HTTP_USER_AGENT')):
            return False
    return View.objects.filter(session_key=request.session._session_key, internal_url=meta.get('PATH_INFO')).count() == 0
    
def view_count(f):
    def render(*args, **kwargs):
            meta = args[0].META
            exclud = Exclude.objects.all()
            
            save = is_new(args[0])
            if save == True:
                view = View()
                view.last_view = datetime.datetime.now()
                view.ip = meta.get('REMOTE_ADDR')
                view.browser = meta.get('HTTP_USER_AGENT')
                view.internal_url = meta.get('PATH_INFO')
                view.lang = meta.get('HTTP_ACCEPT_LANGUAGE')
                try:
                    view.session_key = args[0].session.session_key
                except Exception as e:
                    ajax_log("view_count : %s " % e)
                    views.session_key = "error"
                view.save()
            return f(*args, **kwargs)
            
    return render