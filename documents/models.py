import logging
import os
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from services.singleton import weaviate_service
from utils.choices import FileType
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


# Creates a proxy model for the built-in Django USer model, allowing for customization without changing the underlying database schema
class MyUser(User):
    class Meta:
        proxy = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# Document model with data fields
class Document(models.Model):
    document_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/tempfiles/')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chunks_ids = models.JSONField(default=list, blank=True)

    def __str__(self):
        return str(self.title)

    # Save method override.
    # If the document is being updated, it deletes the existing chunks from Weaviate
    def save(self, *args, **kwargs):
        is_new = self.pk
        if is_new:
            weaviate_service.delete_documents(uuids=self.chunks_ids)
        super().save(*args, **kwargs)
        self.__process_file()

    # Processes the uploaded file. Determines the file type based on the extension. Creates metadata for the document. Uses weaviate_service to create and add documents to Weaviate
    #
    def __process_file(self):
        if not self.file:
            raise ValidationError("No file provided for the document.")
        file_name = self.file.name
        file_path = settings.BASE_DIR / file_name
        file_type = self.__get_file_type(file_name)

        if file_type == "error":
            raise ValidationError("Invalid file")
        try:
            metadata = {
                'title': self.title,
                'description': self.description,
                "file_name": file_name,
                'created_at': str(self.created_at),
                'updated_at': str(self.updated_at),
                'document_id': str(self.document_id)
            }
            docs = weaviate_service.create_documents_from_file(file_path=file_path, file_type=file_type, metadata=metadata)
            ids = weaviate_service.add_documents(docs=docs)
            self.__class__.objects.filter(pk=self.pk).update(chunks_ids=ids)
        except Exception as e:
            self.delete()
            raise e

    # Static method to determine the file type based on the file extension. Maps the file extensions to FileType enum values
    @staticmethod
    def __get_file_type(file_name):
        ext = os.path.splitext(file_name)[1].lower()
        return {
            '.pdf': FileType.PDF,
            '.docx': FileType.DOCX,
            '.xlsx': FileType.XLSX,
            '.csv': FileType.CSV,
            '.txt': FileType.TXT
        }.get(ext, "error")

    # Overrides the delete method to remove associated chunks from Weaviate before deleting the document from the database.
    def delete(self, *args, **kwargs):
        weaviate_service.delete_documents(uuids=self.chunks_ids)
        super().delete(*args, **kwargs)
