from .models import UserData

import re
import datetime
from typing import Dict


class FileExtensionValidator:
    """Utility class for validating file extensions."""

    @staticmethod
    def is_csv(filename):
        """Validates if the file extension is CSV."""
        return filename.endswith(".csv")


class FileHeaderValidator:
    """Utility class for validating file headers."""

    @staticmethod
    def is_valid(file_obj):
        """Validates if the headers in a file are valid."""
        valid_headers = [
            "first_name",
            "last_name",
            "national_id",
            "birth_date",
            "address",
            "country",
            "phone_number",
            "email",
            "finger_print_signature",
        ]
        with open(file_obj, "r") as f:
            headers = f.readline().strip().split(",")
            return set(valid_headers) == set(headers)


class RowDataValidator:
    """Utility class for validating CSV row data."""

    @staticmethod
    def is_valid(row_data: Dict) -> bool:
        """Validates if the row data is valid."""

        # Check if required fields are present and valid
        required_fields = [
            "first_name",
            "last_name",
            "national_id",
            "birth_date",
            "address",
            "country",
            "phone_number",
            "email",
        ]
        if not all(
            row_data.get(field)
            and RowDataValidator.validate_field(field, row_data[field])
            for field in required_fields
        ):
            return False

        finger_print_signature = row_data.get("finger_print_signature", "")
        # TODO:
        # check fingerprint signature is in hash form

        # Check if finger_print_signature is already in UserData
        if not UserData.objects.filter(
            finger_print_signature=finger_print_signature
        ).exists():
            return False

        return True

    @staticmethod
    def validate_field(field_name: str, field_value: str) -> bool:
        """Validates a single field value based on its name."""
        if field_name in ("first_name", "last_name"):
            return field_value.isalpha()
        elif field_name == "national_id":
            return field_value.isdigit()
        elif field_name == "birth_date":
            return RowDataValidator.is_date(field_value)
        elif field_name == "address":
            return field_value.strip() != ""
        elif field_name == "country":
            return field_value.strip() != ""
        elif field_name == "phone_number":
            return field_value.isdigit()
        elif field_name == "email":
            return RowDataValidator.is_email(field_value)
        else:
            return False

    @staticmethod
    def is_date(date_string: str) -> bool:
        """Checks if a string represents a valid date."""
        try:
            datetime.datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_email(email_string: str) -> bool:
        """Checks if a string represents a valid email address."""
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        return re.match(email_regex, email_string) is not None
