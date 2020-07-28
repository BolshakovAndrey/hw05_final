from django.test import TestCase
from django.urls import reverse


class TestUserProfile(TestCase):

    def test_user_profile_creation(self):
        '''
        Testing the creation of a profile for a registered user
        '''
        response = self.client.get(
            reverse('profile', kwargs={'username': 'test_profile'}))
        self.assertEqual(response.status_code, 404)
        self.client.post(reverse('signup'),
                         {'username': 'test_profile',
                          'email': 'testmail@gmail.com',
                          'password1': 'password_test',
                          'password2': 'password_test'}
                         )
        response = self.client.get(
            reverse('profile', kwargs={'username': 'test_profile'}))
        self.assertEqual(response.status_code, 200)