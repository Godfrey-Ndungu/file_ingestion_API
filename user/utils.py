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
        valid_headers = ['first_name', 'last_name', 'national_id', 'birth_date', 'address', 'country', 'phone_number', 'email', 'finger_print_signature']
        with open(file_obj, 'r') as f:
            headers = f.readline().strip().split(',')
            return set(valid_headers) == set(headers)