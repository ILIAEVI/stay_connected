from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User


class LoginViewTests(APITestCase):
    def setUp(self):
        self.user = self.create_user(email="test@gmail.com", password="Password123")
        self.login_url = reverse_lazy('login')

    def create_user(self, email, password):
        return User.objects.create_user(email=email, password=password)

    def test_login_unauthenticated_user(self):
        """
        Test that an unauthenticated user can access the login view and receive tokens.
        """
        response = self.client.post(self.login_url, {
            'email': 'test@gmail.com',
            'password': 'Password123'
        })

        # Check that the response status is 200 OK, and tokens are returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_authenticated_user(self):
        """
        Test that an authenticated user cannot access the login view and gets a 403 response.
        """
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        response = self.client.post(
            self.login_url,
            {'email': 'test@gmail.com', 'password': 'Password123'},
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_without_token(self):
        """
        Test that an unauthenticated user cannot access the login view without providing a token.
        """
        response = self.client.post(self.login_url, {
            'email': 'test@gmail.com',
            'password': 'Password123'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
