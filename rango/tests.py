from django.test import TestCase
from rango.models import Category, Page
from django.core.urlresolvers import reverse

#Chapter 9
import os.path
from rango.models import User, UserProfile
from rango.forms import UserForm, UserProfileForm
from selenium.webdriver.common.keys import Keys
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage

#Chapter 10
from datetime import datetime, timedelta
from django.utils import timezone

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_positive should results True for categories
        where views are zero or positive
        """

        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """

        slug_line_creation checks to make sure that when we add
        a category an appropriate slug line is created
        i.e. "Random Category String" -> "random-category-string"
        """
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')

class IndexViewTests(TestCase):
    #Helper method
    def add_cat(self, name, views, likes):
        c = Category.objects.get_or_create(name=name)[0]
        c.views = views
        c.likes = likes
        c.save()
        return c

    def test_index_view_with_no_categories(self):
        """

        If no questions exist, an appropriate message should be displayed
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """

        Check to make sure that the index has categories displayed
        """

        self.add_cat('test', 1, 1)
        self.add_cat('temp', 1, 1)
        self.add_cat('tmp', 1, 1)
        self.add_cat('tmp test temp', 1, 1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)

class Chapter18Tests(TestCase):
    def test_visit_time_not_in_the_future(self):
        page = Page()
        page.category = Category.objects.get_or_create(name='test')[0]
        page.views = 0
        page.first_visit = timezone.now() + timedelta(days=1)
        page.last_visit = timezone.now() + timedelta(days=5)

        page.save()

        self.assertEqual(
            ((timezone.now() - page.first_visit).days < 0), False)

        self.assertEqual(
            ((timezone.now() - page.last_visit).days < 0), False)

    def test_last_visit_equal_or_after_first_visit(self):
        page = Page()
        page.category = Category.objects.get_or_create(name='test')[0]
        page.views = 0
        page.first_visit = timezone.now()
        page.last_visit = timezone.now() - timedelta(days=5)

        page.save()

        self.assertEqual(
            ((page.last_visit - page.first_visit).days < 0), False)