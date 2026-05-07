from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Project, Task

User = get_user_model()

class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'

    def test_register_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'email@example.com',
            'password': 'strongpassword123',
            'password2': 'strongpassword123'
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertNotIn('password', response.data)

    def test_register_password_mismatch(self):
        data = {
            'username': 'testuser',
            'email': 'email@example.com',
            'password': 'strongpassword123',
            'password2': 'differentpassword123'
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_valid_credentials(self):
        user = User.objects.create_user(username='testuser', password='strongpassword123')

        data = {
            'username': 'testuser',
            'password': 'strongpassword123'
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        user = User.objects.create_user(username='testuser', password='strongpassword123')

        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TaskCRUDTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='strongpassword123'
            )
        self.client.force_authenticate(user=self.user)
        self.list_url = '/api/tasks/'

    def test_list_tasks_authenticated(self):

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_list_tasks_unauthenticated(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task(self):
        data = {
            'title': 'Test Task',
        }

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().owner, self.user)

    def test_update_task(self):
        task = Task.objects.create(
            title='Old Title', owner=self.user
            )
        url = f'/api/tasks/{task.id}/'
            
        response = self.client.patch(url, {'title': 'Updated Title'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Title')

    def test_delete_task(self):
        task = Task.objects.create(
            title='Task to Delete', owner=self.user
            )
        url = f'/api/tasks/{task.id}/'

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class TaskOwnershipTests(APITestCase):

    def setUp(self):
        self.user_a = User.objects.create_user(
            username='userA', password='strongpassword123'
        )
        self.user_b = User.objects.create_user(
            username='userB', password='strongpassword123'
        )
        self.task = Task.objects.create(
            title='Task of userA',
            owner=self.user_a
        )
        self.detail_url = f'/api/tasks/{self.task.id}/'

    def test_owner_can_update(self):
        self.client.force_authenticate(user=self.user_a)

        response = self.client.patch(self.detail_url, {'title': 'Updated by owner'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated by owner')

    def test_non_owner_cannot_update(self):
        self.client.force_authenticate(user=self.user_b)

        response = self.client.patch(self.detail_url, {'title': 'Updated by non-owner'}, format='json')

        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_non_owner_cannot_delete(self):
        self.client.force_authenticate(user=self.user_b)

        response = self.client.delete(self.detail_url)

        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())

    def test_unauthenticated_cannot_update(self):
        self.client.force_authenticate(user=None)

        response = self.client.patch(self.detail_url, {'title': 'Updated by non-owner'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ProjectTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='strongpassword123'
        )
        self.client.force_authenticate(user=self.user)
        self.list_url = '/api/projects/'

    def test_create_project(self):
        data = {
            'name': 'Test Project',
            
        }

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().owner, self.user)

    def test_completion_percentage_empty(self):
        project = Project.objects.create(
            name='Empty Project', owner=self.user
        )
        url = f'/api/projects/{project.id}/'

        response = self.client.get(url)

        self.assertEqual(response.data['completion_percentage'], 0)

    def test_completion_percentage_partial(self):
        project = Project.objects.create(
            name='Partial Project', owner=self.user
        )
        Task.objects.create(
            title='Task 1', project=project, owner=self.user, completed=True
            )
        Task.objects.create(
            title='Task 2', project=project, owner=self.user, completed=False
            )
        url = f'/api/projects/{project.id}/'

        response = self.client.get(url)

        self.assertEqual(response.data['completion_percentage'], 50.0)

    def test_non_owner_cannot_update(self):
        project = Project.objects.create(name='Test Project', owner=self.user)
        user_b = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.force_authenticate(user=user_b)
        url = f'/api/projects/{project.id}/'

        
        response = self.client.patch(url, {'name':'Updated by non Owner'}, format='json')

        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
