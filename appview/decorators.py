# -*- coding: UTF-8 -*-
# YaBlog
#  (c) Regis FLORET 2012 and later
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Regis FLORET 2012 and later BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
AppView
"""

import datetime

from yablog.appview.models import Exclude, View
from yablog.notification import ajax_log

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
