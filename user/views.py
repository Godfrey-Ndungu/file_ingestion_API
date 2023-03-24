from rest_framework import pagination
from rest_framework import filters
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from .models import UserData
from .serializers import UserDataSerializer


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
