Yet Another Django Blog System
==============================

For my own pleasure and my own needs, I wrote a blog program. Who needs a 
very powerful and very efficient and very slow blog program (yes, I'm looking
at you both Wordpress and DotClear). 

YaBlog is not designed to be "Ready To Go" blog but to be a "Wait I'm writing 
the main template"

YaBlog is not for beginners.

Prerequirement
--------------

You must have a little Python knowlege and more serious skills in HTML and 
Django templating system.

You should know how install a Django App.

Optionnal requirement
--------------------

YaBlog works better with:
    * Grappelli : https://github.com/sehmaschine/django-grappelli
    * Filemanager : https://github.com/sehmaschine/django-filebrowser
    * CKEditor : https://github.com/shaunsephton/django-ckeditor

For database evolution, I usually prefer django-evolution.

Local installation
------------------

YaBlog is based upon Django Framework who is wrote in Python. So you need
both Python (>= 2.6): http://www.python.org/ and Django (>= 1.3): 
http://www.djangoproject.com/ .

1) Download with git or unpack a archive in a directory.

2) Install optionnals third party library (YaBlog works fine without).

3) Edit the settings.py file and change the following entries
    - DATABASES
    - SECRET_KEY
    - DONT_USE_CACHE
    - INSTALLED_APPS
    - GRAPPELLI_ADMIN_TITLE

4) Run ./manage.py syncdb

5) To dive into development create two empty files named debug and devlocal.

6) Create the cache table with ./manage.py createcachetable cache. 



