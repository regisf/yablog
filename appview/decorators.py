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
import re

from .models import Exclude, View
from yablog.notification import ajax_log

def is_excludable(request):
    """
    Test if the user is know (using its key)
    """
    meta = request.META
    excluded = Exclude.objects.all()
    excludable = excluded.filter(exclude_IP=meta.get('REMOTE_ADDR')).only('id').count() > 0
    excludable |= View.objects.filter(session_key=request.session._session_key, 
                                     internal_url=meta.get('PATH_INFO')).only('id').count() > 0
    exclusion = excluded.all().only('exclude_regex')
    for exc in list(exclusion):
        if len(exc.exclude_regex.strip()) > 0:
            excludable |= re.search(exc.exclude_regex, meta.get('HTTP_USER_AGENT'), re.I) is not None
    return excludable

def view_count(f):
    """
    Count the number of view regarding the exclusion list or if the user have seen the post
    """
    def render(*args, **kwargs):
        try:
            meta = args[0].META            
            if  is_excludable(args[0]) == False:
                view = View()
                view.last_view = datetime.datetime.now()
                view.ip = meta.get('REMOTE_ADDR')
                view.browser = meta.get('HTTP_USER_AGENT')
                view.internal_url = meta.get('PATH_INFO')
                view.lang = meta.get('HTTP_ACCEPT_LANGUAGE') or "Not set"
                try:
                    view.session_key = args[0].session.session_key
                except Exception as e:
                    ajax_log("app_view.view_count (get session key) : %s " % e)
                    view.session_key = "error"
                view.save()
        except Exception as e:
            # Google which use python urllib make this routine crash. Ignore it.
            ajax_log("app_view.view_count : %s" % e)
        
        return f(*args, **kwargs)
            
    return render
