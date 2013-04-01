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
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

from .models import Preference

class AdminImageWidget(AdminFileWidget):
    """ Affichage d'une miniature dans l'admin """
    def render(self, name, value, attrs=None):
        """ Rendu à la demande """
        output = []
        if value:
            output.append(u'<div>%s</div>' % (value))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        if value and getattr(value, "url", None):
            #l'image mais on pourrait aussi mettre un lien
            img = u'<div><img src="%s" width="128px"/></div>' % (value.url)
            output.append(img)
        return mark_safe(u''.join(output))

class AdminFontWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value:
            output.append(u'<div>%s</div>' % value)
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        if value and getattr(value, "url", None):
            # Get the font

            # On affiche 
            text = u'''<style type="text/css">
            @font-face {
                src: url("/site_media/%s");
                font-family: sample;
            }
            </style>
            <div style="font-family:sample; font-size: 48px;">Portez vieux ce whiskey au juge blond qui fume</div>
            ''' % value
            output.append(text)
        return mark_safe(u''.join(output))

class BaseAdmin(admin.ModelAdmin):
    """ Base pour tout les modules d'administration """
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'background':
            kwargs['widget'] = AdminImageWidget
            kwargs.pop('request', None) #erreur sinon
            return db_field.formfield(**kwargs)
        elif db_field.name == 'font':
            kwargs['widget'] = AdminFontWidget
            kwargs.pop('request', None)
            return db_field.formfield(**kwargs)
        return super(BaseAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(Preference, BaseAdmin)
