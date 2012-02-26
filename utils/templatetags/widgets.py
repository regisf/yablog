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
