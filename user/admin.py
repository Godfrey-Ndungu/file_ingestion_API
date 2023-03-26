from django.contrib import admin
from .models import UserData, FileUpload

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'national_id', 'birth_date', 'address', 'country', 'phone_number', 'email', 'finger_print_signature')
    search_fields = ('first_name', 'last_name', 'national_id', 'email', 'finger_print_signature')
    list_filter = ('country', 'time_added')

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'status', 'time_added')
    list_filter = ('status', 'time_added')
    search_fields = ('file__name',)

