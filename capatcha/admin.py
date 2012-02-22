# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from capatcha.models import Preference

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
