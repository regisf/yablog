# -*- coding: UTF-8 -*-

"""
AppView

Framework to get statistic
"""

from django.contrib import admin
from django.db.models import Q

from appview.models import Exclude, View


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
