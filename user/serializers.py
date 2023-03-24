from rest_framework import serializers
from .models import UserData, FileUpload


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = (
            "first_name",
            "last_name",
            "national_id",
            "birth_date",
            "address",
            "country",
            "phone_number",
            "email",
            "finger_print_signature",
        )
        read_only_fields = fields


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ("id", "file", "status")
        read_only_fields = ("id", "status")
