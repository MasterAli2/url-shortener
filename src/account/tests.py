from django.test import TestCase, Client
from django.contrib.auth.models import User

USERNAME = 'test_user'
PASSWORD = 'testp@assword123'

ACCOUNT_PATH = '/account/'

class AccountViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(ACCOUNT_PATH)
        self.assertEqual(response.status_code, 302)

    def test_loads_for_logged_in_user(self):
        response = self.client.get(ACCOUNT_PATH)
        self.assertEqual(response.status_code, 200)

    def test_valid_password_change(self):
        response = self.client.post(ACCOUNT_PATH, {
            'form_type': 'password',
            'old_password': PASSWORD,
            'new_password1': 'newpassword456!',
            'new_password2': 'newpassword456!',
        })
        self.assertRedirects(response, ACCOUNT_PATH)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword456!'))

    def test_invalid_password_change_mismatch(self):
        response = self.client.post(ACCOUNT_PATH, {
            'form_type': 'password',
            'old_password': PASSWORD,
            'new_password1': 'newpassword456!',
            'new_password2': 'wrongpassword!',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(PASSWORD))

    def test_invalid_password_change_wrong_old_password(self):
        response = self.client.post(ACCOUNT_PATH, {
            'form_type': 'password',
            'old_password': 'wrongpassword',
            'new_password1': 'newpassword456!',
            'new_password2': 'newpassword456!',
        })        
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(PASSWORD))

    def test_valid_profile_update(self):
        response = self.client.post(ACCOUNT_PATH, {
            'form_type': 'profile',
            'username': 'newusername',
        })
        self.assertRedirects(response, ACCOUNT_PATH)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')

    def test_invalid_profile_update_empty_username(self):
        response = self.client.post(ACCOUNT_PATH, {
            'form_type': 'profile',
            'username': '',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, USERNAME)

    def test_delete_account(self):
        response = self.client.post(ACCOUNT_PATH, {
            'form_type': 'delete',
        })
        #self.assertRedirects(response, '/')
        self.assertFalse(User.objects.filter(username='testuser').exists())