from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User

# Create your models here.
class Account(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
