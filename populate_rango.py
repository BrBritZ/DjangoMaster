import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # Through each data structure, and add the data to our models.

    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/",
         "views": 150},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/",
         "views": 85},
        {"title": "Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/",
         "views": 100}]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         "views": 15},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/",
         "views": 3},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/",
         "views": 256}]

    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev",
         "views": 16},
        {"title": "Flask",
         "url": "http://flask.pocoo.org",
         "views": 21}]

    pascal_pages = [
        {"title": "Pascal Tutorial",
         "url": "https://www.tutorialspoint.com/pascal/",
         "views": 11},
        {"title": "Pascal-Programming.info - A Pascal Tutorial",
         "url": "http://pascal-programming.info/",
         "views": 111}]

    perl_pages = [
        {"title": "Beginner's Introduction to Perl",
         "url": "http://www.perl.com/pub/2000/10/begperl1.html",
         "views": 22}]

    php_pages = []

    prolog_pages = []

    postscript_pages = []

    programming_pages = [
        {"title": "Computer Programming",
         "url": "https://www.tutorialspoint.com/computer_programming/",
         "views": 1021}]

    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
            "Django": {"pages": django_pages, "views": 64, "likes": 32},
            "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16},
            "Pascal": {"pages": pascal_pages, "views": 25, "likes": 3},
            "Perl": {"pages": perl_pages, "views": 5, "likes": 1},
            "PHP": {"pages": php_pages, "views": 121, "likes": 30},
            "Prolog": {"pages": prolog_pages, "views": 3, "likes": 0},
            "Postscript": {"pages": postscript_pages, "views": 15, "likes": 1},
            "Programming": {"pages": programming_pages, "views": 3040, "likes": 355}}

    # If you want to add more categories or pages,
    # add them to the dictionaries above

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/
    # for more information about how to iterate over a dictionary properly.

    for cat, cat_data in cats.iteritems():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

#Start execution here!
if __name__ == '__main__':
    print("Starting Rango population scripts...")
    populate()