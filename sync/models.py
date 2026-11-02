from django.db import models
from custom.models import ExamVenue
import uuid

# Create your models here.
class Sync(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	center = models.ForeignKey(ExamVenue)
	destination = models.CharField(max_length=10, choices=(('local', 'LOCAL'), ('remote', 'REMOTE')))
	last_sync = models.DateTimeField(auto_now_add=True)