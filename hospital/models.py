from django.db import models
from base.models import BaseManager, BaseModel
from order.models import Order


class Physician(BaseModel):
    """
    Class for Physician
    """
    firstName = models.CharField(max_length=64, verbose_name="First Name")
    middleName = models.CharField(null=True, blank=True, max_length=64, verbose_name="Middle Name")
    lastName = models.CharField(max_length=64, verbose_name="Last Name")
    address =  models.TextField(verbose_name="Address")
    phoneNumber = models.CharField(max_length=16, verbose_name="Phone Number")

    def __str__(self):
        return f'{self.lastName}, {self.firstName}'

    @property
    def full_name(self):
        """
        Function for full_name
        """
        return f'{self.lastName}, {self.firstName}'


    class Meta:
        verbose_name = 'Physician'
        verbose_name_plural = 'Physicians'

    objects = BaseManager()
    

class Patient(BaseModel):
    firstName = models.CharField(max_length=64, verbose_name="First Name")
    middleName = models.CharField(null=True, blank=True, max_length=64, verbose_name="Middle Name")
    lastName = models.CharField(max_length=64, verbose_name="Last Name")
    address =  models.TextField(verbose_name="Address")
    phoneNumber = models.CharField(max_length=16, verbose_name="Phone Number")

    def __str__(self):
        return f'{self.lastName}, {self.firstName}'

    @property
    def full_name(self):
        return f'{self.lastName}, {self.firstName}'

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    objects = BaseManager()



class Sample(BaseModel):
    sampleId = models.CharField(max_length=255, verbose_name="Sample ID")
    patient = models.ForeignKey(to=Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sampleId}'

    class Meta:
        verbose_name = 'Sample'
        verbose_name_plural = 'Samples'

    objects = BaseManager()
    


class Hospital(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    address = models.TextField(verbose_name="Address")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitals'

    objects = BaseManager()
    

class LaboratoryStorage(BaseModel):
    name = models.CharField(max_length=64, verbose_name="Name")
    location = models.TextField(verbose_name="Location")
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Laboratory Storage'
        verbose_name_plural = 'Laboratory Storage'

    objects = BaseManager()