from .models import UserData
import datetime
import re


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
    def is_valid(row_data):
        """Validates if the row data is valid."""
        first_name = row_data.get("first_name", "").isalpha()
        last_name = row_data.get("last_name", "").isalpha()
        national_id = row_data.get("national_id", "").isdigit()
        birth_date = RowDataValidator.is_date(row_data.get("birth_date", ""))
        address = row_data.get("address", "") != ""
        country = row_data.get("country", "") != ""
        phone_number = row_data.get("phone_number", "").isdigit()
        email = RowDataValidator.is_email(row_data.get("email", ""))
        finger_print_signature = row_data.get("finger_print_signature", "")

        if not all(
            [
                first_name,
                last_name,
                national_id,
                birth_date,
                address,
                country,
                phone_number,
                email,
            ]
        ):
            return False

        if not RowDataValidator.is_finger_print_signature_hashed(
            finger_print_signature
        ):
            return False

        if not UserData.objects.filter(
            finger_print_signature=finger_print_signature
        ).exists():
            return False

        return True

    import re

    def is_finger_print_signature_hashed(signature):
        """Checks if a fingerprint signature is hashed."""
        hash_prefixes = ["$1$", "$2a$", "$2b$", "$2y$"]
        for prefix in hash_prefixes:
            if signature.startswith(prefix):
                # Check if the rest of the signature
                # contains only base64-encoded characters
                regex_pattern = r"^[A-Za-z0-9+/]+={0,2}$"
                return re.match(regex_pattern,
                                signature[len(prefix):]) is not None
        return False

    @staticmethod
    def is_date(date_string):
        """Checks if a string represents a valid date."""
        try:
            datetime.datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_email(email_string):
        """Checks if a string represents a valid email address."""
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        return re.match(email_regex, email_string) is not None
