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
""" Some utils for Django dev """

import os
from PIL import Image, ImageDraw

from django.conf import settings
from django.forms.forms import TextInput
from django import forms
from django.contrib.sitemaps import ping_google

from utils.templatetags.image_tags import utils_thumbnailize
from notification import ajax_log

def utils_thumbnailize_marked(value, size, image):
    """ Creation d'une vignette avec une marque dans l'image. Image est en absolute path """
    thumb_image_name = utils_thumbnailize(value, size, True, True)
    sname, sext = os.path.splitext(os.path.basename(image))
    name, ext = os.path.splitext(os.path.basename(thumb_image_name))
    newname = "%s-%s%s" % (name, sname, ext)
    name = os.path.join(settings.THUMB_DIR, newname)
    if not os.path.exists(name) or settings.DEBUG:
        source_image = Image.open(os.path.join(settings.PROJECT_PATH, thumb_image_name[1:]))
        paste_image = Image.open(image)
        paste_mask = Image.open(image)

        iw, ih = paste_image.size
        sw, sh = source_image.size

        source_image.paste(paste_image, (sw - iw, 0), paste_mask)
        source_image.save(name)
        name = os.path.join(settings.THUMB_URL, os.path.basename(name))
    return utils_thumbnailize(name, size)


def utils_raw_thumbnailize(path, size):
    """ Reduce image size without any other considerations """
    try:
        img = Image.open(path).convert("RGBA")
        img.thumbnail((size,size), Image.ANTIALIAS)
        img.save(path)
    except Exception, e:
        ajax_log("utils_row_thumbnailize : %s" % e)

class MappyWidget(TextInput):
    class Media:
        js = (
            '/site_media/js/jquery-1.4.4.min.js',
            'http://axe.mappy.com/1v1/init/get.aspx?auth=JoPgkTHWjZxBtVzjELVFdk1/6SMZqCTLo6+5T6Rc16ld+SNQeKGh38tMm4ZHhBy0XuuCuJNeT5J9NZw70drtMw==&version=2.01&solution=ajax',
            '/site_media/js/localisation_admin.js',
        )
        css = {
            'screen' : (
                '/site_media/css/admin_style.css',
            )
        }
    
    
class MappyForm(forms.ModelForm):
    latlong = forms.CharField(widget=MappyWidget())


# Code from internet
def ping_all(sitemap_url='http://www.elitemariage.re/sitemap.xml'):
    """
    Pings the popular search engines, Google, Yahoo, ASK, and
    Bing, to let them know that you have updated your
    site's sitemap. Returns successfully pinged servers.
    """
    from django.contrib.sitemaps import ping_google
    SEARCH_ENGINE_PING_URLS = (
        ('google', 'http://www.google.com/webmasters/tools/ping'),
        ('yahoo', 'http://search.yahooapis.com/SiteExplorerService/V1/ping'),
        ('ask', 'http://submissions.ask.com/ping'),
        ('bing', 'http://www.bing.com/webmaster/ping.aspx'),
    )
    successfully_pinged = []
    for (site, url) in SEARCH_ENGINE_PING_URLS:
        try:
            ping_google(sitemap_url=sitemap_url, ping_url=url)
            pinged = True
        except:
            pinged = False
        if pinged:
            successfully_pinged.append(site)
    return successfully_pinged