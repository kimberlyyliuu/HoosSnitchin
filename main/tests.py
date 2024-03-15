from django.test import TestCase
from main.models import CustomUser

# Create your tests here.

# Test Set 1: Test the CustomUser model
class CustomUserModelTests(TestCase):
    # Test 1-1: Creation
    def test_creation(self):
        user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword',
            first_name='Kevin',
            last_name='Cha'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Kevin')
        self.assertEqual(user.last_name, 'Cha')
        self.assertTrue(user.check_password('testpassword'))
        self.assertFalse(user.is_site_admin)
        self.assertTrue(user.is_active)


# Test Set 2: Test Login/Logout functionality
class AccessControlTests(TestCase):
    # Test 2-1: Test login
    def test_login(self):
        user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword1234',
            first_name='Kevin',
            last_name='Cha'
        )
        user.save()
        response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'testpassword1234'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)