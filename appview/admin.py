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

from django.contrib import admin
from django.db.models import Q

from .models import Exclude, View


class ViewAdmin(admin.ModelAdmin):
    list_display = ['ip', 'session_key', 'internal_url', 'last_view', 'admin_get_browser',]
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
