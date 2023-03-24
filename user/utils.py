class FileExtensionValidator:
    """Utility class for validating file extensions."""

    @staticmethod
    def is_csv(filename):
        """Validates if the file extension is CSV."""
        return filename.endswith(".csv")
