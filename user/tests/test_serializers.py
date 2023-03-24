from django.test import TestCase
from user.serializers import UserDataSerializer, FileUploadSerializer
from user.models import UserData, FileUpload


class TestSerializers(TestCase):
    def test_user_data_serializer(self):
        # Create test data
        user_data = UserData.objects.create(
            first_name="John",
            last_name="Doe",
            national_id="1234567890",
            birth_date="1990-01-01",
            address="123 Main St",
            country="USA",
            phone_number="555-1234",
            email="john.doe@example.com",
            finger_print_signature="abc123",
        )

        # Create serializer instance
        serializer = UserDataSerializer(instance=user_data)

        # Check serialized data
        expected_data = {
            "first_name": "John",
            "last_name": "Doe",
            "national_id": "1234567890",
            "birth_date": "1990-01-01",
            "address": "123 Main St",
            "country": "USA",
            "phone_number": "555-1234",
            "email": "john.doe@example.com",
            "finger_print_signature": "abc123",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_file_upload_serializer(self):
        # Create test data
        file_upload = FileUpload.objects.create(
            file="path/to/file.txt",
            status="pending",
        )

        # Create serializer instance
        serializer = FileUploadSerializer(instance=file_upload)

        # Check serialized data
        # status is processing once the object is saved
        # django appends / to file
        expected_data = {
            "id": file_upload.id,
            "file": "/path/to/file.txt",
            "status": "processing",
        }
        self.assertEqual(serializer.data, expected_data)
