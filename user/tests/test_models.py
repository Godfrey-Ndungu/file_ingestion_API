from django.test import TestCase
from user.models import UserData, FileUpload


class UserDataTestCase(TestCase):
    def setUp(self):
        self.user_data = UserData.objects.create(
            first_name="John",
            last_name="Doe",
            national_id="123456789",
            birth_date="2000-01-01",
            address="123 Main St.",
            country="USA",
            phone_number="1234567890",
            email="john.doe@example.com",
            finger_print_signature="abc123",
        )

    def test_user_data_created_successfully(self):
        self.assertEqual(UserData.objects.count(), 1)

    def test_is_finger_print_signature_unique_returns_true(self):
        self.assertTrue(self.user_data.is_finger_print_signature_unique())

    def test_is_finger_print_signature_unique_returns_false(self):
        # create another user data with the same finger print signature
        UserData.objects.create(
            first_name="Jane",
            last_name="Doe",
            national_id="987654321",
            birth_date="2000-01-01",
            address="123 Main St.",
            country="USA",
            phone_number="1234567890",
            email="jane.doe@example.com",
            finger_print_signature="abceew123",
        )
        self.assertTrue(self.user_data.is_finger_print_signature_unique())


class FileUploadTestCase(TestCase):
    def setUp(self):
        self.file_upload = FileUpload.objects.create(
            file="uploads/test_file.csv")

    def test_file_upload_created_successfully(self):
        self.assertEqual(FileUpload.objects.count(), 1)

    def test_start_processing_transition(self):
        self.assertEqual(self.file_upload.status,
                         FileUpload.FILE_STATUS_PENDING)

    def test_mark_failed_transition_from_pending(self):
        file_upload = FileUpload.objects.create(file="uploads/test_file.csv")
        file_upload.mark_failed()
        self.assertEqual(file_upload.status, FileUpload.FILE_STATUS_FAILED)

    def test_mark_failed_transition_from_processing(self):
        self.file_upload.mark_failed()
        self.assertEqual(self.file_upload.status,
                         FileUpload.FILE_STATUS_FAILED)

    def test_mark_processed_transition(self):
        self.file_upload.start_processing()
        self.file_upload.mark_processed()
        self.assertEqual(self.file_upload.status,
                         FileUpload.FILE_STATUS_PROCESSED)

    def test_mark_processing_failed_transition_from_pending(self):
        file_upload = FileUpload.objects.create(file="uploads/test_file.csv")
        file_upload.start_processing()
        file_upload.mark_processing_failed()
        self.assertEqual(file_upload.status, FileUpload.FILE_STATUS_FAILED)

    def test_mark_processing_failed_transition_from_processing(self):
        self.file_upload.start_processing()
        self.file_upload.mark_processing_failed()
        self.assertEqual(self.file_upload.status,
                         FileUpload.FILE_STATUS_FAILED)

    def test_filename(self):
        self.assertEqual(self.file_upload.filename(), "test_file.csv")
