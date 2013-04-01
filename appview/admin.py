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

Framework to get statistic
"""
import re

from django.contrib import admin
from django.db.models import Q

from .models import Exclude, View


class ViewAdmin(admin.ModelAdmin):
    list_display = ['ip', 'session_key', 'internal_url', 'last_view', 'lang', 'admin_get_browser',]
    actions = ['add_exclusion', 'add_exclusion_and_delele', 'delete_excluded',]
    
    def add_exclusion(self, request, queryset):
        c = 0
        for query in queryset:
            if Exclude.objects.filter(Q(exclude_IP=query.ip) | Q(exclude_regex=query.browser)).count() == 0:
                Exclude(exclude_IP=query.ip, exclude_regex=query.browser, name="No name").save()
                c += 1
        if not c:
            self.message_user(request, "Exclusion list added. Please edit them.")
        else:
            self.message_user(request, "No exclusion add because they were inside yet.")
                
    add_exclusion.short_description = u"Add entries to exclusion list"
    
    def add_exclusion_and_delele(self, request, queryset):
        c=0
        for query in queryset:
            if Exclude.objects.filter(Q(exclude_IP=query.ip) | Q(exclude_regex=query.browser)).count() == 0:
                Exclude(exclude_IP=query.ip, exclude_regex=query.browser, name="No name").save()
                query.delete()
                c += 1
        if c == 0:
            self.message_user(request, "Exclusion list added. Please edit them.")
        else:
            self.message_user(request, "No exclusion add because they were inside yet.")
    add_exclusion_and_delele.short_description = u"Add entries to exclusion list and delete them"
        
    def delete_excluded(self, request, queryset):
        count = 0
        for query in queryset:
            for ex in Exclude.objects.all():
                if ex.exclude_IP == query.ip or ex.match(query.browser):
                    query.delete()
                    count += 1
        self.message_user(request, "%d entries were deleted" % count)
    delete_excluded.short_description = "Delete entries with exclusion rules."
        
class ExcludeAdmin(admin.ModelAdmin):
    list_display = ['name', 'exclude_IP', 'exclude_regex', ]
    
admin.site.register(Exclude, ExcludeAdmin)
admin.site.register(View, ViewAdmin)


def is_mobile(browser):
    """ Test if the browser is a Mobile Browser """
    return re.search(r'webos|Symbianos|iphone|android|blackberry|opera\smini|opera\smobi|palm|^nokia|^samsung|^lg|^sonyericsson', browser, re.I) is not None
        

def stats(request):
    """ 
    Display statistics for the web site
    """
    from django.shortcuts import render_to_response, RequestContext
    
    views = list(View.objects.all().only('internal_url', 'browser'))
    urls = {}
    mob_vs_desk = { 'desktop': 0, 'mobile': 0 }
    for view in views:
        if is_mobile(view.browser):
            mob_vs_desk['mobile'] += 1
        else:
            mob_vs_desk['desktop'] += 1
            
        if not urls.has_key(view.internal_url):
            urls[view.internal_url] = 0
        urls[view.internal_url] += 1
    stats = []
    count = 0
    for url in urls:
        stats.append({'url': url, 'count': urls[url]})
        count += urls[url]
    stats = sorted(stats, key=lambda k: k['count'], reverse=True)
    return render_to_response('admin/appview/view/display_stats.html', 
                              RequestContext(request, { 'stats' : stats,
                                                        'total' : count,
                                                        'views':  mob_vs_desk
                                                      }
                                             )
                              )


def flush_views(request):
    """ 
    Remove views with exclusion rules
    @TODO: Use admin.Model instead
    """
    from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect

    views = list(View.objects.all())
    excluded = list(Exclude.objects.all())
    ips = []
    exclude_brows = []
    for view in excluded:
#        ips.append(view.exclude_IP)
        exclude_brows.append(view.exclude_regex)
    
    deleted = []
    for view in list(views.all()):
        for exc in exclude_brows:
            if re.search(exc, view.browser, re.I):
                deleted.append(view.pk)
            
    deleted = views.filter(Q(ip__in=ips) | Q(pk__in=deleted))
    if len(deleted) == 0:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    if request.method == 'POST':
        deleted.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
        
    return render_to_response('admin/appview/view/delete_flush_confirm.html', 
                              RequestContext(request, {
                                    'todelete':deleted
                              }))
    
def history(request):
    """
    Display stats by day
    """
    from django.shortcuts import render_to_response, RequestContext
    
    views = list(View.objects.all())
    year = {}
    for v in views:
        if not year.has_key(v.last_view.year):
            year[v.last_view.year] = {}
            
        if not v.last_view.month in year[v.last_view.year]:
            year[v.last_view.year][v.last_view.month] = {}

        if not year[v.last_view.year][v.last_view.month].has_key(v.last_view.day):
            year[v.last_view.year][v.last_view.month][v.last_view.day] = 0
        year[v.last_view.year][v.last_view.month][v.last_view.day] += 1
    return render_to_response('admin/appview/view/history_stat.html', RequestContext(request, { 'stats': year }))
