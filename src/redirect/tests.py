from django.test import TestCase, Client
from django.contrib.auth.models import User
from redirect.models import ShortLink

USERNAME = 'test_user'
OTHER_USERNAME = 'other_user'
PASSWORD = 'testp@assword123'
DASHBOARD_PATH = '/dashboard/'
TEST_CODE = 'abc123'
TEST_URL = 'https://example.com'

class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.other_user = User.objects.create_user(username=OTHER_USERNAME, password=PASSWORD)
        self.client.login(username=USERNAME, password=PASSWORD)

    # Access
    def test_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(DASHBOARD_PATH)
        self.assertEqual(response.status_code, 302)

    def test_loads_for_logged_in_user(self):
        response = self.client.get(DASHBOARD_PATH)
        self.assertEqual(response.status_code, 200)

    # Create
    def test_create_valid_shortlink(self):
        self.client.post(DASHBOARD_PATH, {
            'form_type': 'create',
            'code': TEST_CODE,
            'url': TEST_URL,
        })
        self.assertTrue(ShortLink.objects.filter(code=TEST_CODE, owner=self.user).exists())

    def test_create_invalid_url(self):
        self.client.post(DASHBOARD_PATH, {
            'form_type': 'create',
            'code': TEST_CODE,
            'url': 'not-a-url',
        })
        self.assertFalse(ShortLink.objects.filter(code=TEST_CODE).exists())

    def test_create_invalid_code_characters(self):
        invalid_code = '/invalid code!'
        self.client.post(DASHBOARD_PATH, {
            'form_type': 'create',
            'code': invalid_code,
            'url': TEST_URL,
        })
        self.assertFalse(ShortLink.objects.filter(code=invalid_code).exists())

    def test_create_duplicate_code(self):
        ShortLink.objects.create(code=TEST_CODE, url=TEST_URL, owner=self.user)
        self.client.post(DASHBOARD_PATH, {
            'form_type': 'create',
            'code': TEST_CODE,
            'url': 'https://other.com',
        })
        self.assertEqual(ShortLink.objects.filter(code=TEST_CODE).count(), 1)

    def test_created_link_belongs_to_user(self):
        self.client.post(DASHBOARD_PATH, {
            'form_type': 'create',
            'code': TEST_CODE,
            'url': TEST_URL,
        })
        link = ShortLink.objects.get(code=TEST_CODE)
        self.assertEqual(link.owner, self.user)

    # Delete
    def test_delete_own_shortlink(self):
        ShortLink.objects.create(code=TEST_CODE, url=TEST_URL, owner=self.user)
        self.client.post(DASHBOARD_PATH, {
            'form_type': 'delete',
            'code': TEST_CODE,
        })
        self.assertFalse(ShortLink.objects.filter(code=TEST_CODE).exists())

    def test_cannot_delete_other_users_shortlink(self):
        ShortLink.objects.create(code=TEST_CODE, url=TEST_URL, owner=self.other_user)
        self.client.post(DASHBOARD_PATH, {
            'form_type': 'delete',
            'code': TEST_CODE,
        })
        self.assertTrue(ShortLink.objects.filter(code=TEST_CODE).exists())

    # Display
    def test_only_shows_own_shortlinks(self):
        ShortLink.objects.create(code='mine', url=TEST_URL, owner=self.user)
        ShortLink.objects.create(code='theirs', url=TEST_URL, owner=self.other_user)
        response = self.client.get(DASHBOARD_PATH)
        links = response.context['links']
        self.assertTrue(all(link.owner == self.user for link in links))