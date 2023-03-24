from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import UserData


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
