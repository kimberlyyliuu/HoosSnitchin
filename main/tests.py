from django.utils import timezone

from main.models import CustomUser, Document, Report, Event
from django.test import TestCase


# Test Set 1: Test the CustomUser model
class CustomUserModelTests(TestCase):
    # Test 1-1: Creation
    def test_creation(self):
        user = CustomUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            first_name="Kevin",
            last_name="Cha",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "Kevin")
        self.assertEqual(user.last_name, "Cha")
        self.assertTrue(user.check_password("testpassword"))
        self.assertFalse(user.is_site_admin)
        self.assertTrue(user.is_active)


# Test Set 2: Test the Report model
class ReportModelTests(TestCase):
    # Test 2-1: Creation
    def test_creation_ReportModelTests(self):
        user = CustomUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            first_name="Kevin",
            last_name="Cha",
        )
        event = Event.objects.create(title="Test Event", description="Test Description")
        report = Report.objects.create(description="Test Report", user_id=1, event_id=1)
        self.assertEqual(report.description, "Test Report")
        self.assertEqual(report.user_id, 1)
        self.assertEqual(report.event_id, 1)


# Test Set 3: Test the Document model
class DocumentModelTests(TestCase):
    # Test 3-1: Creation
    def test_creation_DocumentModelTests(self):
        datetime = timezone.now()
        document = Document.objects.create(
            document="Test Document",
            created_at=datetime,
            title="Test Title",
        )
        self.assertEqual(document.document, "Test Document")
        self.assertEqual(document.created_at, datetime)
        self.assertEqual(document.title, "Test Title")


# Test Set 4: Test the Event model
class EventModelTests(TestCase):
    # Test 4-1: Creation
    def test_creation_EventModelTests(self):
        event = Event.objects.create(title="Test Event", description="Test Description")
        self.assertEqual(event.title, "Test Event")
        self.assertEqual(event.description, "Test Description")


# Test Set 5: Test Views
class ViewsTests(TestCase):
    # Test 5-1: Test the index view Basic
    def test_index_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")

    # Test 5-2: Test the document upload view Basic
    def test_document_upload_view(self):
        event = Event.objects.create(title="Test Event", description="Test Description")
        response = self.client.get("/report/1/upload/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/document_upload.html")

    # Test 5-3: Test the report upload view Basic
    def test_report_upload_view(self):
        event = Event.objects.create(title="Test Event", description="Test Description")
        response = self.client.get("/report/event1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/report_upload.html")


# Test Set 6: Test Forms
class FormsTests(TestCase):
    # Test 6-1: Test the report form
    def test_report_form(self):
        user = CustomUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            first_name="Kevin",
            last_name="Cha",
        )
        event = Event.objects.create(title="Test Event", description="Test Description")

        response = self.client.post(
            "/report/event1/",
            {"description": "Test Report Description", "event": event.title},
        )
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.context['form'].cleaned_data['description'], 'Test Report Description')

    # Test 6-2: Test the document form
    def test_document_form(self):
        user = CustomUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            first_name="Kevin",
            last_name="Cha",
        )
        event = Event.objects.create(title="Test Event", description="Test Description")
        report = Report.objects.create(
            description="Test Report Description",
            user=user,
            event=event,
        )
        response = self.client.post(
            "/report/1/upload/", {"files": "TestDoc.txt", "report_id": 1}
        )
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.context['form'].cleaned_data['file_field'], 'Test Document')


"""
# Test Set X: Test Login/Logout functionality
class AccessControlTests(TestCase):
    # Test 2-1: Test login
    def test_login(self):
        CustomUser = get_user_model()
        testuser = CustomUser.objects.create_user(
            username='testuser',
            password='asjdh341qwasdlk',
            first_name='Kevin',
            last_name='Cha'
        )
        response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'asjdh341qwasdlk'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].firstname, 'Kevin')
        self.assertTrue(response.context['user'].is_authenticated)
"""
