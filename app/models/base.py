from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    soft_deleted = models.BooleanField(default=False) # Adiciona o campo de soft delete

    class Meta:
        abstract = True
        ordering = ['-created_at']