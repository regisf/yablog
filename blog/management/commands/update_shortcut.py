# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand
from yablog.blog.models import Tag, Categorie, sanitize_name

class Command(BaseCommand):
    help = "Upgrade Tag and Categories"
    
    def handle(self, *args, **options):
        print "Doing tags"
        for t in Tag.objects.all():
            print "\tSave", t.Nom, 'to', sanitize_name(t.Nom)
            t.save()
        print "Done"
            
        print;print
        print "Doing categories"
        for c in Categorie.objects.all():
            print "\tSaving", c.Nom, 'to', sanitize_name(c.Nom)
            c.save()
        print "Done"
        
        print;print "That's all folks"            