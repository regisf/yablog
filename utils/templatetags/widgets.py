# -*- coding: UTF-8 -*-

"""
Widgets divers pour l'affichage dans les pages
"""

from time import strftime

from django import template
from django.forms.widgets import Select
from django.utils.safestring import mark_safe

from shop.forms import SelectDateWidget

from utils.templatetags.choices import COUNTRIES
register = template.Library()

@register.simple_tag
def form_date_widget(date, name):
    """ Affiche la date sous forme de trois select """
    return SelectDateWidget(years=range(1900, int(strftime('%Y')) - 10)).render(name=name, value=date)


@register.simple_tag
def form_country_list_widget(selected, name):
    """ Création d'un widget affichant la liste des pays """
    jscript = """<script type="text/javascript">
    $(document).ready(function() {
        $("select[name=%s]").after('<img src="/site_media/images/flags/%s.png" alt="drapeau" class="drapeau" width="16" height="11" /> ');
        $("select[name=%s]").change(function() {
            flag = $(this).attr("value").toLowerCase();
           $("img.drapeau").attr("src",'/site_media/images/flags/'+flag+'.png'); 
        });
    });
    </script>
    """ % (name, selected.lower(), name)

    output = u'<select name="%s" style="width: 200px;">' % unicode(name)
    for country in COUNTRIES:
        sel = ''
        if selected.lower() == country[0].lower():
            sel = u' selected="selected"'
        output += u'<option value="%s"%s>%s</option>\n' % (country[0], sel, country[1])
    output += u'</select>'
    output += jscript
    return mark_safe(output)
