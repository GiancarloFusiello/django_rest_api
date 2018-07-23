import uuid

from django.db import models


class Creator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)

class Prezi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.URLField()
    title = models.CharField(max_length=120)
    created_at = models.DateTimeField()
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
