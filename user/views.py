from rest_framework.parsers import FormParser, MultiPartParser
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework import pagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from .models import UserData, FileUpload
from .serializers import UserDataSerializer, FileUploadSerializer
from .utils import FileExtensionValidator


class UserPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 1000


class UserDataViewSet(ListModelMixin, GenericViewSet):
    """
    A viewset for listing user data.

    This viewset allows clients to retrieve a list of user data using various filters, search criteria,
    and sorting options. The `UserDataSerializer` is used to serialize the user data.

    Available filter options include `first_name`, `last_name`, `phone_number`, `email`, and `birth_date`.
    One can also search for users based on any of these fields using the `search` query parameter.
    Sorting can be performed on the `first_name`, `last_name`, and `birth_date` fields using the `ordering`
    query parameter.

    Additionally, clients can filter users based on a range of birth dates using the `birth_date` query parameter.
    This parameter should be specified as a comma-separated string with two values: the start date and the end date.

    By default, this viewset uses the `UserPagination` class for pagination.
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
    search_fields = ["first_name", "last_name",
                     "phone_number", "email", "birth_date"]
    ordering_fields = ["first_name", "last_name", "birth_date"]
    pagination_class = UserPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        birth_date_range = self.request.query_params.get("birth_date", None)
        if birth_date_range:
            start_date, end_date = birth_date_range.split(",")
            queryset = queryset.filter(
                birth_date__range=[start_date, end_date])

        return queryset


class FileUploadViewSet(ModelViewSet):
    """
        Viewset for uploading CSV files.

        Attributes:
            parser_classes (list): List of parser classes to use.
            serializer_class (Serializer): Serializer class to use.
            queryset (QuerySet): QuerySet of objects to use.

        Methods:
            create(request): Creates a new file upload object and saves the uploaded file.

        Raises:
            ValidationError: If the uploaded file is not a CSV file.

        Returns:
            Response: HTTP response object containing the serialized file upload object.
    """
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.all()

    def create(self, request):
        file_obj = request.FILES.get("file")
        extension_validator = FileExtensionValidator()

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

        return Response(FileUploadSerializer(file_upload).data)
