""" Patients Resolvers """
from lms_core import settings
from django.db.models import Q
from hospital.models import Patient
from datetime import date, datetime
from ariadne import convert_kwargs_to_snake_case
from ariadne import ObjectType, QueryType, MutationType


query = QueryType()
mutation = MutationType()
patient = ObjectType("Patient")


@query.field("patients")
@convert_kwargs_to_snake_case
def resolve_patients(obj, info, **kwargs):
    offset = 0
    limit = settings.DEFAULT_LIMIT
    queryset = Patient.objects.all()

    if 'sort' in kwargs and 'order_by' in kwargs:
        if kwargs['sort']=="ASC" and kwargs['order_by']:
            queryset = Patient.objects.all().order_by(kwargs['order_by'])
        elif kwargs['sort']=="DESC" and kwargs['order_by']:
            queryset = Patient.objects.all().order_by('-'+kwargs['order_by'])
    else:
        queryset = Patient.objects.all()
    if queryset:
        if 'limit' in kwargs:
            limit = kwargs['limit']
        if 'offset' in kwargs:
            offset = kwargs['offset']
    if 'search' in kwargs:
        queryset = queryset.filter(
                Q(phoneNumber__icontains=kwargs['search'])
                | Q(firstName__icontains=kwargs['search'])
                | Q(lastName__icontains=kwargs['search'])
                | Q(middleName__icontains=kwargs['search'])
                | Q(address__icontains=kwargs['search'])
                | Q(created__icontains=kwargs['search'])
            )[offset: offset+ limit]
    queryset = queryset[offset: offset+ limit]
    return queryset


@mutation.field("createPatient")
def resolve_create_patient(obj, info, **kwargs):
    patient = Patient.objects.create(**kwargs)
    return patient


@mutation.field("deletePatient")
@convert_kwargs_to_snake_case
def resolve_delete_patient(obj, info, **kwargs):
    try:
        patient_data = Patient.objects.get(id=kwargs['id'])
        patient_data.isDeleted = True
        patient_data.save()
    except Patient.DoesNotExist:
        return False
    return True


@query.field("getPatient")
@convert_kwargs_to_snake_case
def resolve_get_patient(obj, info, **kwargs):
    try:
        patient = Patient.objects.get(id=kwargs['id'])
    except Patient.DoesNotExist:
        return None
    return patient



@mutation.field("updatePatient")
# @convert_kwargs_to_snake_case
def resolve_update_patient(obj, info, **kwargs):
    try:
        data_patient = Patient.objects.get(id=kwargs['id'])
        data_patient.firstName = kwargs['firstName']
        data_patient.middleName = kwargs['middleName']
        data_patient.lastName = kwargs['lastName']
        data_patient.address = kwargs['address']
        data_patient.phoneNumber = kwargs['phoneNumber']
        data_patient.save()

    except Patient.DoesNotExist:
        return None
    return data_patient

@query.field("searchPatient")
@convert_kwargs_to_snake_case
def resolve_search_patient(obj, info, **kwargs):
    try:
        patients = Patient.objects.filter(
                Q(phoneNumber__icontains=kwargs['search'])
                | Q(firstName__icontains=kwargs['search'])
                | Q(lastName__icontains=kwargs['search'])
                | Q(middleName__icontains=kwargs['search'])
                | Q(address__icontains=kwargs['search'])
                | Q(created__icontains=kwargs['search'])
            )
    except Patient.DoesNotExist:
        return None
    return patients

resolvers = [query, mutation, patient,]