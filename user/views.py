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
