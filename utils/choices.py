from django.db import models


class FileType(models.TextChoices):
    PDF = 'pdf', 'PDF'
    DOCX = 'docx', 'DOCX'
    XLSX = 'xlsx', 'XLSX'
    CSV = 'csv', 'CSV'
    TXT = 'txt', 'TXT'
