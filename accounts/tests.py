import json

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from rest_framework import status

from .models import User, SignUpCode, SocialToken
from .auth import passwd_token


class UserTestCase(TestCase):
    """User test case"""

    def setUp(self):
        self.user = User.objects.create(
            firstName='User',
            lastName='User',
            username='user',
            password='p455w0rd',
            birthday=timezone.datetime(year=1986, month=5, day=12),
            phone='55 4351 8691'
        )
        self.user.set_password(self.user.password)

        self.social_token = SocialToken.objects.create(
            social='facebook', token='tk-100', user=self.user
        )
        self.signup_code = SignUpCode.objects.create(email='user2@mail.org')
        self.token = passwd_token(self.user)
        self.client = Client()

    def tearDown(self):
        self.social_token.delete()
        self.user.delete()
        self.signup_code.delete()

    def test_a_password_hash(self):
        self.assertTrue(self.user.password.startswith(
            'pbkdf2_sha256') and len(self.user.password) == 78)

    def test_b_signup_exists(self):
        path = reverse('signup-exists')

        response = self.client.post(path, json.dumps({
            'username': 'user2'
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_c_signup_mail(self):
        path = reverse('signup-mail')

        response = self.client.post(path, json.dumps({
            'email': 'user2@mail.org'
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_d_signup_check(self):
        path = reverse('signup-check')

        response = self.client.post(path, json.dumps({
            'email': self.signup_code.email,
            'code': self.signup_code.code
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_e_signup(self):
        path = reverse('accounts-signup')

        response = self.client.post(path, json.dumps({
            'firstName': 'User 2',
            'lastName': 'User 2',
            'username': 'user2',
            'password': 'p455w0rd',
            'email': self.signup_code.email,
            'birthday': '1987-06-20',
            'phone': '55 4530 2942',
            'code': self.signup_code.code
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_f_signin(self):
        path = reverse('accounts-signin')

        response = self.client.post(path, json.dumps({
            'username': 'user', 'password': 'p455w0rd'
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        return response.json().get('token')

    def test_g_social_signup(self):
        path = reverse('social-signup')

        response = self.client.post(path, json.dumps({
            'firstName': 'User 3',
            'lastName': 'User 3',
            'username': 'user3',
            'email': 'user3@mail.org',
            'birthday': '1987-06-20',
            'phone': '55 4530 2942',

            'social': 'facebook',
            'token': 'tk-101'
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_h_social_signin(self):
        path = reverse('social-signin')

        response = self.client.post(path, json.dumps({
            'social': 'facebook',
            'username': 'user', 'token': 'tk-100'
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        return response.json().get('token')

    def test_i_passwd_change(self):
        path = reverse('passwd-change')
        token = self.test_f_signin()

        response = self.client.post(path, json.dumps({
            'old': 'p455w0rd', 'new': '12345678'
        }), content_type='application/json',
            HTTP_AUTHORIZATION='Token %s' % token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_j_passwd_mail(self):
        path = reverse('passwd-mail')

        response = self.client.post(path, json.dumps({
            'username': 'user'
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_k_passwd_check(self):
        path = reverse('passwd-check')

        response = self.client.post(path,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token %s' % self.token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_l_passwd_reset(self):
        path = reverse('passwd-reset')

        response = self.client.post(path, json.dumps({
            'password': 'p455w0rd'
        }), content_type='application/json',
            HTTP_AUTHORIZATION='Token %s' % self.token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_f_signin()
