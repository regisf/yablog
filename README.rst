Yet Another Django Blog System
==============================

For my own pleasure and my own needs, I wrote a blog program. Who needs a 
very powerful and very efficient and very slow blog program (yes, I'm looking
at you both Wordpress and DotClear). 

YaBlog is not:
    * Designed to be "Ready To Go" blog but to be a "Wait I'm writing  the main template"
    * For beginners.

YaBlog is:
    * Written in Python
    * Fast
    * Minimalistic

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
    * DATABASES: The default is MyBlog.db with SQLite3 engine
    * SECRET_KEY: 
    * DONT_USE_CACHE: Set it to True to avoid caching system
    * INSTALLED_APPS: Uncomment lines for optionnal libraries
    * GRAPPELLI_ADMIN_TITLE: Change this for your real blog name. If you're using grappelli of course.

4) Run ./manage.py syncdb

5) To dive into development create two empty files named debug and devlocal.

6) Create the cache table with ./manage.py createcachetable cache

7) type ./manage.py runserver and open a browser at http://localhost:8000/admin/
   For Windows user (especially with Windows 7) prefer http://127.0.0.1:8000/admin/
   Enter your login name and password and go to Blog->Preferences. Create a new
   entry and enter your blog name and it's subtitle. Save your preferences.
   
   If you don't add your preferences, YaBlog will create them for you.

8) That's all... You can start to design your template (see Templates).

9) If you want to add commentaries to the blog. Go to the admin -> capatcha and
   create a new preference row. Upload the font (TTF) and the background. Save it.
   (see Capatcha). 
   
   Go the notification -> preferences -> add and add a new preference. Enter the 
   server name (this is for administraton), the email of the sender, the SMTP user
   the SMTP user password, the SMTP server domain (eg: smtp.myblog.com).
   
   If your smtp don't need user authentification check Anonymous.
   
   (see Notification)



Templates
---------
Todo
   
Capatcha
--------
Todo

Notification
------------
Todo

Production Installation
-----------------------
Todo

Database evolution
------------------
Todo


