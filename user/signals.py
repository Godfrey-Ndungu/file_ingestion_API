from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import FileUpload
from .tasks import process_uploaded_file


@receiver(post_save, sender=FileUpload)
def start_file_upload_signal(sender, instance, created, **kwargs):
    if created:
        process_uploaded_file.delay(instance.id)
