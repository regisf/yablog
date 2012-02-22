from django.contrib import admin

from notification.models import *

class BaseAdmin(admin.ModelAdmin):

    class Media:
        js = (
                '/site_media/js/jquery-1.4.2.min.js',
                '/site_media/js/tiny_mce/tiny_mce.js',
                '/site_media/js/textareas.js',
                '/site_media/js/admin/notification.js',
        )

class PreferenceAdmin(BaseAdmin):
    list_display = ('name', 'default2string', 'sendmail', 'anonymous', 'username', 'offuscate_pass', 'server',)

admin.site.register(Preference, PreferenceAdmin)
admin.site.register(Template)
admin.site.register(MailingList, BaseAdmin)
