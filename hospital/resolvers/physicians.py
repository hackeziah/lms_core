""" Physician Resolvers """

from django.db.models import Q

from hospital.models import Physician
from datetime import date, datetime
from ariadne import convert_kwargs_to_snake_case
from ariadne import ObjectType, QueryType, MutationType

from lms_core import settings


query = QueryType()
mutation = MutationType()
physician = ObjectType("Physician")


@query.field("physicians")
@convert_kwargs_to_snake_case
def resolve_physicians(obj, info, **kwargs):
    offset = 0
    limit = settings.DEFAULT_LIMIT
    queryset = Physician.objects.all()

    if 'sort' in kwargs and 'order_by' in kwargs:
        if kwargs['sort']=="ASC" and kwargs['order_by']:
            queryset = Physician.objects.all().order_by(kwargs['order_by'])
        elif kwargs['sort']=="DESC" and kwargs['order_by']:
            queryset = Physician.objects.all().order_by('-'+kwargs['order_by'])
    else:
        queryset = Physician.objects.all()
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


@mutation.field("createPhysician")
def resolve_create_patient(obj, info, **kwargs):
    physician = Physician.objects.create(**kwargs)
    return physician


@mutation.field("deletePhysician")
@convert_kwargs_to_snake_case
def resolve_delete_patient(obj, info, **kwargs):
    try:
        physician = Physician.objects.get(id=kwargs['id'])
        physician.isDeleted = True
        physician.save()
    except Physician.DoesNotExist:
        return False
    return True


@query.field("getPhysician")
@convert_kwargs_to_snake_case
def resolve_get_physician(obj, info, **kwargs):
    try:
        physician = Physician.objects.get(id=kwargs['id'])
    except physician.DoesNotExist:
        return None
    return physician



@mutation.field("updatePhysician")
@convert_kwargs_to_snake_case
def resolve_update_physician(obj, info, **kwargs):
    try:
        data_physician = Physician.objects.get(id=kwargs['id'])
        data_physician.firstName = kwargs['first_name']
        data_physician.middleName = kwargs['middle_name']
        data_physician.lastName = kwargs['last_name']
        data_physician.address = kwargs['address']
        data_physician.phoneNumber = kwargs['phone_number']
        data_physician.save()

    except Physician.DoesNotExist:
        return None
    return data_physician


@query.field("searchPhysician")
@convert_kwargs_to_snake_case
def resolve_search_physician(obj, info, **kwargs):
    try:
        physicians = Physician.objects.filter(
                Q(phoneNumber__icontains=kwargs['search'])
                | Q(firstName__icontains=kwargs['search'])
                | Q(lastName__icontains=kwargs['search'])
                | Q(middleName__icontains=kwargs['search'])
                | Q(address__icontains=kwargs['search'])
                | Q(created__icontains=kwargs['search'])
            )
    except Physician.DoesNotExist:
        return None
    return physicians


resolvers = [query, mutation, physician,]