import io
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.test import APITestCase

from user.models import UserData
from user.models import FileUpload

from user.serializers import FileUploadSerializer


class UserDataViewSetTests(APITestCase):
    def setUp(self):
        self.user_data_1 = UserData.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            email="john.doe@example.com",
            birth_date="1990-01-01",
            finger_print_signature="abceew123eeeee",
        )
        self.user_data_2 = UserData.objects.create(
            first_name="Jane",
            last_name="Doe",
            phone_number="0987654321",
            email="jane.doe@example.com",
            birth_date="1995-01-01",
            finger_print_signature="asedbceew123",
        )

    def test_list_user_data(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_search_user_data(self):
        url = reverse("user-list")
        # Search by first name
        query_params = {"search": "John"}
        response = self.client.get(url, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

        # Search by last name
        query_params = {"search": "Doe"}
        response = self.client.get(url, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_order_user_data(self):
        url = reverse("user-list")
        # Order by first name ascending
        query_params = {"ordering": "first_name"}
        response = self.client.get(url, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["first_name"], "Jane")

        # Order by first name descending
        query_params = {"ordering": "-first_name"}
        response = self.client.get(url, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["first_name"], "John")


class FileUploadViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_upload_file(self):
        file_data = io.BytesIO(b"csv_file_content")
        file = SimpleUploadedFile(
            "file.csv", file_data.getvalue(), content_type="text/csv"
        )
        response = self.client.post(
            "/v1/file-upload/", {"file": file}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FileUpload.objects.count(), 1)
        self.assertEqual(
            response.data, FileUploadSerializer(
                FileUpload.objects.first()).data
        )

    def test_upload_invalid_file_type(self):
        file_data = io.BytesIO(
            b"invalid_file_content"
        )  # replace with your file content
        file = SimpleUploadedFile(
            "file.txt", file_data.getvalue(), content_type="text/plain"
        )
        response = self.client.post(
            "/v1/file-upload/", {"file": file}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {
                "error": "Invalid file type. Only CSV files are allowed."}
        )
        self.assertEqual(FileUpload.objects.count(), 0)
