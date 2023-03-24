import logging
from celery import shared_task
from django.core.files.storage import default_storage
from .utils import RowDataValidator,FileHeaderValidator
from .models import UserData,FileUpload
import csv


logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_uploaded_file(self,id):
    
    file = FileUpload.objects.filter(id=id).first()
    if file:
        file_path=str(file.file.path)
        
        # check headers
        if not FileHeaderValidator.is_valid(file_path):
                    raise ValueError("Invalid file headers.")
        else:
            """Task to process uploaded file."""
            try:
                # Open the uploaded CSV file and validate its headers
                with default_storage.open(file_path, mode='r') as f:
                    reader = csv.DictReader(f)
                    # Iterate over each row in the CSV file, validate its data, and save it to the UserData model
                    for row in reader:
                        if RowDataValidator.is_valid(row):
                            user_data = UserData(
                                first_name=row['first_name'],
                                last_name=row['last_name'],
                                national_id=row['national_id'],
                                birth_date=row['birth_date'],
                                address=row['address'],
                                country=row['country'],
                                phone_number=row['phone_number'],
                                email=row['email'],
                                finger_print_signature=row['finger_print_signature']
                            )
                            user_data.save()
                
                    
            except Exception as exc:
                logger.error(f"Failed to process uploaded file: {exc}")
                raise self.retry(exc=exc, max_retries=3)