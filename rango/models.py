from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    # additional attribute for max value length
    max_length = 128

    name = models.CharField(max_length=max_length, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):

        #Checking that views cannot be zero
        if self.views < 0:
            self.views = 0
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def __unicode__(self):  # For Python 2
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    last_visit = models.DateTimeField(default=timezone.now())
    first_visit = models.DateTimeField(default=timezone.now())

    def save(self, *args, **kwargs):

        #Checking that time cannot be the future
        if (timezone.now() - self.last_visit).days < 0:
            self.last_visit = timezone.now()
        if (timezone.now() - self.first_visit).days < 0:
            self.first_visit = timezone.now()

        # Checking that last visit time have to equal or after first visit
        if ((self.last_visit - self.first_visit).days < 0):
            self.last_visit = self.first_visit

        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def __unicode__(self): # For Python 2
        return self.title

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

    # Remember of you use Python 2.7.x, define __unicode__ too!
    def __unicode__(self):
        return self.user.username