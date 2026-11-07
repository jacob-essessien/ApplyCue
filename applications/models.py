from django.conf import settings
from django.db import models


class JobApplication(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_applications",
    )
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.company} - {self.role}"