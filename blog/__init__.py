# -*- coding: UTF-8 -*-

import unicodedata
import re

   
# Code from internet
def ping_all(sitemap_url='http://www.regisblog.fr/sitemap.xml'):
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
    
def sanitize_name(name):
    """ Ensure to remove all non-alphanum characters """
    name = unicodedata.normalize('NFKD', name).encode('ascii','ignore')
    for c in "&\"'()'ç=²¹~#{}[]+°$£^*µ%!§:/;.,?":
        name = name.replace(c,"")            
    name = name.lower().strip()
    name = re.sub("\s","-",re.sub("\s+$","",name))
    return name
