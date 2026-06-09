from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Task


User = get_user_model()


class HealthApiTests(APITestCase):
    def test_health_check_returns_ok(self):
        response = self.client.get(reverse('health-check'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')

    def test_health_check_rejects_post(self):
        response = self.client.post(reverse('health-check'), {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AuthApiTests(APITestCase):
    def test_register_creates_user_and_token(self):
        response = self.client.post(
            reverse('auth-register'),
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'password': 'strong-pass-123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'alice')

        user = User.objects.get(username='alice')
        self.assertTrue(user.check_password('strong-pass-123'))
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_login_returns_token(self):
        user = User.objects.create_user(
            username='alice',
            password='strong-pass-123',
        )
        token = Token.objects.create(user=user)

        response = self.client.post(
            reverse('auth-login'),
            {'username': 'alice', 'password': 'strong-pass-123'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], token.key)
        self.assertEqual(response.data['user']['username'], 'alice')

    def test_logout_deletes_token(self):
        user = User.objects.create_user(
            username='alice',
            password='strong-pass-123',
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.post(reverse('auth-logout'))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(user=user).exists())

        response = self.client.get(reverse('auth-me'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskApiTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            username='alice',
            password='strong-pass-123',
        )
        self.bob = User.objects.create_user(
            username='bob',
            password='strong-pass-123',
        )
        self.alice_token = Token.objects.create(user=self.alice)
        self.bob_token = Token.objects.create(user=self.bob)

    def authenticate_as(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_task_list_requires_authentication(self):
        response = self.client.get(reverse('task-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_saves_task_for_authenticated_user(self):
        self.authenticate_as(self.alice_token)

        response = self.client.post(
            reverse('task-list'),
            {'title': 'Write API tests'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(title='Write API tests')
        self.assertEqual(task.user, self.alice)
        self.assertFalse(task.completed)

    def test_task_list_only_returns_current_users_tasks(self):
        Task.objects.create(user=self.alice, title='Alice task')
        Task.objects.create(user=self.bob, title='Bob task')
        self.authenticate_as(self.alice_token)

        response = self.client.get(reverse('task-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Alice task')

    def test_update_task_changes_only_owned_task(self):
        task = Task.objects.create(user=self.alice, title='Alice task')
        self.authenticate_as(self.alice_token)

        response = self.client.patch(
            reverse('task-detail', kwargs={'pk': task.pk}),
            {'completed': True},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_other_users_task_is_not_visible(self):
        task = Task.objects.create(user=self.bob, title='Bob task')
        self.authenticate_as(self.alice_token)

        response = self.client.get(reverse('task-detail', kwargs={'pk': task.pk}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_list_rejects_put(self):
        self.authenticate_as(self.alice_token)

        response = self.client.put(
            reverse('task-list'),
            {'title': 'Unexpected'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
