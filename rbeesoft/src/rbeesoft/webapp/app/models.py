import uuid
from django.db import models


class LogOutputModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    mode = models.CharField(max_length=8, editable=False, null=False, choices=[
        ('info', 'info'),
        ('warning', 'warning'),
        ('error', 'error'),
    ], default='info')
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=1024, editable=False, null=False)

    def __str__(self):
        return f'[{self.timestamp}] - [{self.mode}]: {self.message}'