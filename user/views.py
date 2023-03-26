from django.db import transaction
from django.http import Http404

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import filters
from rest_framework import pagination
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import UserData, FileUpload
from .serializers import UserDataSerializer, FileUploadSerializer
from .utils import FileExtensionValidator


class UserPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 1000


class UserDataViewSet(ListModelMixin, GenericViewSet):
    """
    API Documentation:

        API Root: /v1/

        Endpoint: /v1/user-data/
        Methods: GET
        Description: Get a list of user data based on various filters, search criteria, and sorting options.

        Query Parameters:
        - first_name: Filter by user's first name
        - last_name: Filter by user's last name
        - phone_number: Filter by user's phone number
        - email: Filter by user's email
        - birth_date: Filter by user's birth date within a specified range (comma-separated start and end dates)
        - search: Search for users based on any of the filter fields
        - ordering: Sort the results by first_name, last_name, or birth_date in ascending or descending order

        Expected Response:
        {
            "count": 2,
            "next": "http://localhost:8000/v1/users/?page=2",
            "previous": null,
            "results": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "national_id": "1234567890",
                    "birth_date": "1990-01-01",
                    "address": "123 Main St",
                    "country": "USA",
                    "phone_number": "123-456-7890",
                    "email": "john.doe@example.com",
                    "finger_print_signature": "abc123"
                },
                {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "national_id": "0987654321",
                    "birth_date": "1992-05-15",
                    "address": "456 Oak St",
                    "country": "USA",
                    "phone_number": "555-555-5555",
                    "email": "jane.doe@example.com",
                    "finger_print_signature": "def456"
                }
            ]
        }
    """

    serializer_class = UserDataSerializer
    queryset = UserData.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "birth_date",
    ]
    search_fields = ["first_name", "last_name", "phone_number", "email", "birth_date"]
    ordering_fields = ["first_name", "last_name", "birth_date"]
    pagination_class = UserPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        birth_date_range = self.request.query_params.get("birth_date", None)
        if birth_date_range:
            start_date, end_date = birth_date_range.split(",")
            queryset = queryset.filter(birth_date__range=[start_date, end_date])

        return queryset


class FileUploadViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    API Documentation
        ------------------

        API root: /v1/

        Endpoints:
        - POST /file-upload/
            Creates a new file upload object and saves the uploaded file.
            Request parameters:
                - file: the CSV file to be uploaded.
            Response:
                - 201 CREATED: Returns the serialized file upload object on success.
                - 400 BAD REQUEST: Returns an error message if the file is not uploaded, or if the uploaded file is empty or not a CSV file.

        - GET /file-upload/<pk>/
            Retrieves a specific file upload object.
            Request parameters:
                - pk: the primary key of the file upload object.
            Response:
                - 200 OK: Returns the serialized file upload object on success.
                - 404 NOT FOUND: Returns an error message if the specified file upload object does not exist.

        - GET /file-upload/
            Retrieves a list of file upload objects.
            Response:
                - 200 OK: Returns a paginated list of serialized file upload objects on success.
                - 404 NOT FOUND: Returns an error message if there are no file upload objects.

        Example Requests and Responses:
        -------------------------------

        POST /v1/file-upload/
        Request:
            Content-Disposition: form-data; name="file"; filename="example.csv"
            Content-Type: text/csv

            id,name,age
            1,Alice,25
            2,Bob,30

        Response:
            HTTP 201 Created
            Content-Type: application/json

            {
                "id": 1,
                "file": "http://localhost:8000/media/example.csv",
                "status": "PENDING"
            }

        GET /v1/file-upload/1/
        Response:
            HTTP 200 OK
            Content-Type: application/json

            {
                "id": 1,
                "file": "http://localhost:8000/media/example.csv",
                "status": "PENDING"
            }

        GET /v1/file-upload/
        Response:
            HTTP 200 OK
            Content-Type: application/json

            {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "id": 1,
                        "file": "http://localhost:8000/media/example.csv",
                        "status": "PENDING"
                    }
                ]
            }

    """

    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileUploadSerializer
    permission_classes = [AllowAny]
    queryset = FileUpload.objects.all()

    def create(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        extension_validator = FileExtensionValidator()

        # Check if file exists and is not empty
        if not file_obj:
            return Response(
                {"error": "No file uploaded."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif file_obj.size == 0:
            return Response(
                {"error": "File is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate file extension
        if not extension_validator.is_csv(file_obj.name):
            return Response(
                {"error": "Invalid file type. Only CSV files are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save file upload object
        with transaction.atomic():
            file_upload = FileUpload(
                file=file_obj, status=FileUpload.FILE_STATUS_PENDING
            )
            file_upload.save()

        return Response(
            FileUploadSerializer(file_upload).data,
            status=status.HTTP_201_CREATED
                        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            file_upload = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FileUploadSerializer(file_upload)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FileUploadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FileUploadSerializer(queryset, many=True)
        return Response(serializer.data)
