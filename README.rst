==============================
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
    
You can see a live example at http://www.regisblog.fr/ (in french)

--------------
Prerequirement
--------------

You must have a little Python knowlege and more serious skills in HTML and 
Django templating system.

You should know how install a Django App.

---------------------
Optionnal requirement
---------------------

YaBlog works better with:
    * Grappelli : https://github.com/sehmaschine/django-grappelli
    * Filemanager : https://github.com/sehmaschine/django-filebrowser
    * CKEditor : https://github.com/shaunsephton/django-ckeditor

For database evolution, I usually prefer django-evolution.

------------------
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
   
   If your smtp don't need user authentification check Anonymous (that's the case
   at home)
   
   (see Notification)

---------
Templates
---------
With Django you don't have to reinvent the wheel. YaBlog use the Django template
system with few calls to the API.


All templates name are registred in the settings.py file in BLOG_CONFIG class
(~ line 200).

For the full featured blog create 9 templates :
    * index.html : the blog home page
    * all.html : display all blog entries
    * tags.html : display all blog entries by tag
    * categories.html : display all blog entries by category
    * bydate.html : display all blog entries for a particular month or a particular year
    * search.html : display all blog entries after a search
    * post.html : display a particular post

For a simple blog, YaBlog need only one template :  index.html, the blog home
page.

In the Template Context Processor, YaBlog define a blog object. All the API
calls are from this object (e.g.: {{ blog.do_that }})

blog.get_title : The blog title
blog.get_subtitle : The blog subtitle
blog.last_posts : The blog last posts limited with the Preference.maxLatestDisplayed
                  entry (default is 5)
blog.get_posts: Get all posts
blog.get_categories: Get all categories
blog.get_tags: Get all post tags with there weight as tuple
blog.get_history: Get all history as a dictionnary. Year are keys and the values
                  a month list.
                  

Using get_tags (doing a tag cloud):
    This API was thougth for a tag cloud. blog.get_tags will return a list of
    tuple containing all tags : (count, size, tag)
    count: How many post have this tag
    size: the tag weight from 0 to 5
    tag: the tag name.
    
    You should see a example implementation in root.html 
   
--------
Capatcha
--------
For commentaries, user must identify themself as human if they want to leave a message.

Configuration
-------------
Go to the /admin/capatcha/preferences and add a entry.
You have to upload the captcha font and the captcha background.
Save this preference. That's all.

Using in template
-----------------
You must load captcha template tags with {% load capatcha_tags %}.
Create captcha somewhere in the template with {% create_capatcha %}. This tag
will create a new context key named capatcha. To display it simply type :
<img src="{{ capatcha.path }}" alt="Nothing to say :)"/>
<input type="text" name="capatcha" />

When sending the post commentary, Yablog will compare if the given capatcha
is well typed.

------------
Notification
------------
The notification module you to send emails that informs you about the blog life.
It is based on the Django Templating system and is able to send UTF-8 emails.

Configuration
-------------
The first step is to create a Notification preference. In the administation (/admin/)
select Notification application en click on "Preferences". Create a new entry.
Yablog will try to get the first preference entry.
Fill the form with appropriated entries:
    * Preference name
    * Sender email
    * SMTP server informations (login, pasword, address, port)
    * Is this server account is the default account.
    
If your email server doesn't need authentification, select "Anonymous" field.
Save this preference.
    

Create at least one template
----------------------------
At least the Notification app need *one* template : newcomment as defined with 
BLOG_CONFIG.EmailTemplates.newcommentary in settings.py file.
In Notification admin create a new template named "newcomment". This template
will inform you that a new commentary is waiting for you moderation.



You can now create a new template for your blog and send it in production.