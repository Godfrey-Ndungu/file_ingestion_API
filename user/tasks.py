import logging
from celery import shared_task

from .helpers import FileReader
from .utils import FileHeaderValidator, RowDataValidator
from .models import FileUpload, UserData

logger = logging.getLogger()


@shared_task()
def process_uploaded_file(id):
    file = FileUpload.objects.filter(id=id).first()
    if not file:
        return

    file_path = str(file.file.path)
    try:
        headers_are_valid = FileHeaderValidator.is_valid(file_path)
        if not headers_are_valid:
            raise ValueError("Invalid file headers.")

        # Read the file using FileReader
        rows = FileReader.read_file(file_path)

        # Iterate over each row in the CSV file,
        # validate its data, and save it to the UserData model
        for row in rows:
            if RowDataValidator.is_valid(row):
                user_data = UserData(
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    national_id=row["national_id"],
                    birth_date=row["birth_date"],
                    address=row["address"],
                    country=row["country"],
                    phone_number=row["phone_number"],
                    email=row["email"],
                    finger_print_signature=row["finger_print_signature"],
                )
                user_data.save()

    except ValueError as exc:
        logger.error(f"Failed to process uploaded file: {exc}")
        raise process_uploaded_file.retry(exc=exc, max_retries=3)

    except Exception as exc:
        logger.error(f"Failed to process uploaded file: {exc}")
        raise process_uploaded_file.retry(exc=exc, max_retries=3)

    logger.info(f"Successfully processed uploaded file: {file_path}")
    return "File processed successfully!"
