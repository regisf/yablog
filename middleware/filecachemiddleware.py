# -*- coding: utf-8 -*-
# YaBlog
# Fast cache for Django
#  (c) Regis FLORET
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
# DISCLAIMED. IN NO EVENT SHALL Regis FLORET BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.#
# This file is under BSD

import os, time
from hashlib import md5

from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache

class FastCacheMiddleware(object):
    def __init__(self, ):
        self.cache_dir = getattr(settings, 'CACHE_DIR', None)
        self.timeout = getattr(settings, 'CACHE_TIMEOUT', None)
        self.use_django_cache = getattr(settings, 'CACHE_USE_DJANGO', False)
        self.exclude_path = getattr(settings, 'CACHE_EXCLUDE_PATH', [])
        self.replace_csrf = getattr(settings, 'CACHE_REPLACE_CSRF', False)

    def _is_image(self, path):
        return path.startswith(settings.MEDIA_URL) or path.startswith(settings.STATIC_URL)

    def process_request(self, request):
        """ IF request is a POST, pass threw """
        if self.cache_dir:
            if request.method == 'GET':
                if request.path_info in self.exclude_path:
                    return None

                if self._is_image(request.path_info):
                    return None

                if request.path_info.startswith('/admin'):
                    return None

                cached_file = os.path.join(self.cache_dir, "{0}.html".format(md5(request.path_info).hexdigest())) + request.META['QUERY_STRING']
                if self.use_django_cache:
                    content = cache.get(cached_file)
                    if content is not None:
                        return HttpResponse(cache.get(cached_file))

                if os.path.exists(cached_file):
                    mtime = int(os.stat(cached_file).st_mtime)
                    now = int(time.time())
                    if now - mtime < self.timeout:
                        try:
                            # urllib2 (used by Google Bot) is well know to not handle the session.
                            request.session['cached'] = True
                        except:
                            pass

                        return HttpResponse(open(cached_file,'r').read())
        return None

    def process_response(self, request, response):
        if request.method != 'GET' or not response['Content-Type'].startswith('text/html') or response.status_code != 200:
            """ Not a GET, not a HTML file and not OK response : Do nothing """
            return response
        try:
            # urllib2 (used by Google Bot) is well know to not handle the session.
            if request.session.has_key('cached'):
                del request.session['cached']
                return response
        except:
            pass

        cached_file = os.path.join(self.cache_dir, "{0}.html".format(md5(request.path_info).hexdigest())) + request.META['QUERY_STRING']
        if self.use_django_cache:
            cache.set(cached_file,response.content)
        else:
            open(cached_file, 'w').write(response.content)

        return response
