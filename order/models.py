from re import T
from statistics import mode
from django.db import models
from base.models import BaseModel, BaseManager

# Create your models here.
class Order(BaseModel):

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    RECEIVED = 'RECEIVED'
    STORED = 'STORED'

    STATUS = (
      (RECEIVED, 'RECEIVED'),
      (STORED, 'STORED'),
    )
    internalId = models.CharField(max_length=255, verbose_name="Internal ID")
    dateSampleTaken =  models.DateField(verbose_name="Date Sample Taken")
    sample = models.ForeignKey(to='hospital.Sample', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(choices=STATUS, default="RECEIVED", max_length=10)
    hospital = models.ForeignKey(to='hospital.Hospital', on_delete=models.CASCADE, null=True, blank=True)
    physician = models.ForeignKey(to='hospital.Physician', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.internalId}-{self.dateSampleTaken}'

    objects = BaseManager()
    