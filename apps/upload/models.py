from django.db import models
from django.core.exceptions import ValidationError
import hashlib
import uuid

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='reports/')
    file_hash = models.CharField(max_length=64, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def generate_file_hash(self, file):
        """Generate a SHA-256 hash for the given file."""
        hash_sha256 = hashlib.sha256()
        for chunk in file.chunks():
            hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def save(self, *args, **kwargs):
        if not self.file_hash:
            # Generate the file hash
            self.file_hash = self.generate_file_hash(self.file)
        
        # Check if the file hash already exists in the database
        existing_reports = Report.objects.filter(file_hash=self.file_hash)
        if existing_reports.exists():
            existing_files_info = "\n".join(
                [f"{report.file.name.split('/')[1]} uploaded at: {report.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"
                 for report in existing_reports]
            )
            raise ValidationError(f"This report already exists:\n{existing_files_info}.")
        
        super().save(*args, **kwargs)
