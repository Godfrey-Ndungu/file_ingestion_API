from django.db import models
import os
from django_fsm import FSMField, transition


class Base(models.Model):
    time_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UserData(Base):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=50)
    birth_date = models.DateField()
    address = models.TextField()
    country = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    finger_print_signature = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["-id"]

    def is_finger_print_signature_unique(self):
        """
        Checks whether the finger print signature of
        this model instance is unique across all existing instances.

        Returns:
            True if the finger print signature is unique, False otherwise.
        """
        # Retrieve all instances with the same finger print signature
        matching_instances = self.__class__.objects.filter(
            finger_print_signature=self.finger_print_signature
        )

        # Exclude this instance from the list of
        # matching instances (if it exists)
        if self.pk is not None:
            matching_instances = matching_instances.exclude(pk=self.pk)

        # Return True if no other instance has the
        # same finger print signature, False otherwise
        return not bool(matching_instances)

    def save(self, *args, **kwargs):
        if not self.is_finger_print_signature_unique():
            # handle uniqueness violation
            pass
        super().save(*args, **kwargs)


class FileUpload(Base):
    FILE_STATUS_PENDING = "pending"
    FILE_STATUS_PROCESSING = "processing"
    FILE_STATUS_PROCESSED = "processed"
    FILE_STATUS_FAILED = "failed"
    FILE_STATUSES = (
        (FILE_STATUS_PENDING, "Pending"),
        (FILE_STATUS_PROCESSING, "Processing"),
        (FILE_STATUS_PROCESSED, "Processed"),
        (FILE_STATUS_FAILED, "Failed"),
    )

    file = models.FileField(upload_to="media/uploads/")
    status = FSMField(default=FILE_STATUS_PENDING, choices=FILE_STATUSES)

    @transition(field=status,
                source=FILE_STATUS_PENDING, target=FILE_STATUS_PROCESSING)
    def start_processing(self):
        pass

    @transition(
        field=status,
        source=[FILE_STATUS_PENDING, FILE_STATUS_PROCESSING],
        target=FILE_STATUS_FAILED,
    )
    def mark_failed(self):
        pass

    @transition(
        field=status,
        source=FILE_STATUS_PROCESSING, target=FILE_STATUS_PROCESSED
    )
    def mark_processed(self):
        pass

    @transition(
        field=status,
        source=[FILE_STATUS_PROCESSING, FILE_STATUS_PROCESSED],
        target=FILE_STATUS_FAILED,
    )
    def mark_processing_failed(self):
        pass

    def save(self, *args, **kwargs):
        # Save the file first
        super().save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)
