# -*- coding: UTF-8 -*-

import os

from PIL import Image

from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings

register = template.Library()

@register.filter
@stringfilter
def utils_thumbnailize(value, size=100, crop=False, force=False):
    """ Création d'une image à la taille voulue et renvoie le nom """
    size = size, size
    name = os.path.basename(value)
    dname = os.path.dirname(value)
    img = None
    filename, extension = os.path.splitext(name)
    name = "%s.png" % filename
    output_file = os.path.join(settings.THUMB_DIR, 'thumb_%dx%d_%s' % (size[0], size[1], name))
    url = os.path.join(settings.THUMB_URL, 'thumb_%dx%d_%s' % (size[0], size[1], name))
    real_output_file = os.path.join(settings.THUMB_DIR, output_file)
    if not os.path.exists(real_output_file) or force or settings.DEBUG:
        try:
            img = Image.open(os.path.join(settings.PROJECT_PATH, value[1:])).convert("RGBA")
        except Exception, e:
            img = Image.open(os.path.join(settings.PROJECT_PATH, settings.NO_IMAGE_PATH[1:]))

        if size is None:
            size = img.size[0] / 3, img.size[1] / 3
        img.thumbnail(size, Image.ANTIALIAS)
    
        if not crop:
            maxsize = max(img.size)
            # Image trop fine : on la met dans un cadre transparent
            tmpimg = Image.new("RGBA", (maxsize, maxsize), 0)
            w, h = img.size
            x = (maxsize - w) / 2
            y = (maxsize - h) / 2
            tmpimg.paste(img, (x, y))
            img = tmpimg
            filename, extension = os.path.splitext(real_output_file)
            real_output_file = "%s.png" % (filename)
        img.save(real_output_file)
    return url.replace('\\','/')

@register.filter
@stringfilter
def utils_thumbnailize_complete(value, size=100):
    """ Création d'une vignette carrée, même si l'image ne l'est pas """
    return utils_thumbnailize(value, size, True)


