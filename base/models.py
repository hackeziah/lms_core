from statistics import mode
from django.db import models
import uuid



class BaseManager(models.Manager):
    def get_queryset(self):
        return super(BaseManager, self).get_queryset().filter(isDeleted=False)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateField(auto_now_add=True)
    lastUpdated = models.DateField(auto_now=True)
    isDeleted = models.BooleanField(default=False)

    
    class Meta:
        abstract = True
 