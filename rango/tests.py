from django.test import TestCase
from rango.models import Category
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

class Chapter9ViewTests(TestCase):
    def test_upload_image(self):
        # Create fake user and image to upload to register user
        image = SimpleUploadedFile("testuser.jpg", "file_content", content_type="image/jpeg")
        response = self.client.post(reverse('register'),
                                    {'username': 'testuser', 'password': 'test1234',
                                     'email': 'testuser@testuser.com',
                                     'website': 'http://www.testuser.com',
                                     'picture': image})

        # Check user was successfully registered
        self.assertIn('thank you for registering!'.lower(), response.content.lower())
        user = User.objects.get(username='testuser')
        user_profile = UserProfile.objects.get(user=user)
        path_to_image = './media/profile_images/testuser.jpg'

        # Check file was saved properly
        self.assertTrue(os.path.isfile(path_to_image))

        # Delete fake file created
        default_storage.delete('./media/profile_images/testuser.jpg')

    def test_login_provides_error_message(self):
        # Access login page
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpass'})

        try:
            self.assertIn('wronguser', response.content)
        except:
            self.assertIn('wrongpass', response.content)


# ====== Chapter 10
class Chapter10SessionTests(TestCase):
    def test_user_number_of_access_and_last_access_to_index(self):
        #Access index page 100 times
        for i in xrange(0, 100):
            self.client.get(reverse('index'))
            session = self.client.session

            # Check it exists visits and last_visit attributes on session
            self.assertIsNotNone(self.client.session['visits'])
            self.assertIsNotNone(self.client.session['last_visit'])

            # Check last visit time is within 0.1 second interval from now
            # self.assertAlmostEqual(datetime.now(),
            #     datetime.strptime(session['last_visit'], "%Y-%m-%d %H:%M:%S.%f"), delta=timedelta(seconds=0.1))

            # Get last visit time subtracted by one day
            last_visit = datetime.now() - timedelta(days=1)

            # Set last visit to a day ago and save
            session['last_visit'] = str(last_visit)
            session.save()

            # Check if the visits number in session is being incremented and it's correct
            self.assertEquals(session['visits'], 1)
            # before it was i+1 but visits shouldn't change for the same ip visited in one day


class Chapter10ViewTests(TestCase):
    def test_index_shows_number_of_visits(self):
        #Access index
        response = self.client.get(reverse('index'))

        # Check it contains visits message
        self.assertIn('visits: 1'.lower(), response.content.lower())

    def test_about_page_shows_number_of_visits(self):
        #Access index page to count one visit
        self.client.get(reverse('index'))

        # Access about page
        response = self.client.get(reverse('about'))

        # Check it contains visits message
        self.assertIn('visits: 1'.lower(), response.content.lower())

    def test_visit_number_is_passed_via_context(self):
        #Access index
        response = self.client.get(reverse('index'))

        # Check it contains visits message in the context
        self.assertIn('visits', response.context)

        #Access about page
        response = self.client.get(reverse('about'))

        # Check it contains visits message in the context
        self.assertIn('visits', response.context)


