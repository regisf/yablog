# -*- coding: utf-8 -*-
# YaBlog
#  (c) Regis FLORET
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
# DISCLAIMED. IN NO EVENT SHALL Regis FLORET BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# -*- coding: utf-8 -*-

"""
This is the plugin system
In the post.content you may load the plugins tag with {% load plugins %}
and then load you plugin with {% load_plugin plugin_name %}
"""

import os
import imp
import sys

from django import template

register = template.Library()

def _load_plugin(plugin):
    """ Load a plugin """
    from django.conf import settings
    try:
        module = sys.modules[u"yablog.plugins.%s" % plugin]
    except (KeyError, ImportError):
        plugin_path = os.path.join(settings.BLOG_CONFIG.PluginPath)
        file_pointer, pathname, desc = imp.find_module(plugin, [plugin_path,])
        module = imp.load_module(plugin, file_pointer, pathname, desc)
    return module

def install_plugins_models(installed_app, config):
    """ Add to INSTALLED_APPS the plugin """
    for plugin in config.Plugins:
        installed_app += 'yablog.plugins.%s' % plugin, # do not erase the comma
    return installed_app

def install_plugins_admin():
    """ Install admin.py for all plugins """
    from django.conf import settings
    for plugin in os.listdir(settings.BLOG_CONFIG.PluginPath):
        if os.path.isdir(os.path.join(settings.BLOG_CONFIG.PluginPath, plugin)):
            load_plugin(plugin)
        

@register.tag
def load_plugin(_unused_parser, token):
    """ template tag that load a plugin """
    _unused_name, pluginname = token.split_contents()
    class LoadPluginNode(template.Node):
        """ Node for the load_plugin template tag """
        def render(self, context):
            context[pluginname] = _load_plugin(pluginname).create(context)
            return ''
        
    return LoadPluginNode()

