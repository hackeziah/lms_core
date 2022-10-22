""" Order Resolvers """
from random import sample
from hospital.models import Hospital, Patient, Physician, Sample
from lms_core import settings
from django.db.models import Q
from order.models import Order
from datetime import date, datetime
from ariadne import convert_kwargs_to_snake_case
from ariadne import ObjectType, QueryType, MutationType



query = QueryType()
mutation = MutationType()
order = ObjectType("Order")


@query.field("orders")
@convert_kwargs_to_snake_case
def resolve_orders(obj, info, **kwargs):
    offset = 0
    limit = settings.DEFAULT_LIMIT
    queryset = Order.objects.all()
    if 'sort' in kwargs and 'order_by' in kwargs:
        if kwargs['sort']=="ASC" and kwargs['order_by']:
            queryset = Order.objects.all().order_by(kwargs['order_by'])
        elif kwargs['sort']=="DESC" and kwargs['order_by']:
            queryset = Order.objects.all().order_by('-'+kwargs['order_by'])
    else:
        queryset = Order.objects.all()
    if queryset:
        if 'limit' in kwargs:
            limit = kwargs['limit']
        if 'offset' in kwargs:
            offset = kwargs['offset']
    if 'search' in kwargs:
        queryset = queryset.filter(
                Q(name__icontains=kwargs['search'])
                | Q(physician__firstName__icontains=kwargs['search'])
                | Q(physician__lastName__icontains=kwargs['search'])
                | Q(physician__middleName__icontains=kwargs['search'])
                | Q(hospital__name__icontains=kwargs['search'])
                | Q(hospital__address__icontains=kwargs['search'])
                | Q(sample__sampleId__icontains=kwargs['search'])
                | Q(sample__patient__firstName__icontains=kwargs['search'])
                | Q(sample__patient__lastName__icontains=kwargs['search'])
                | Q(sample__patient__middleName__icontains=kwargs['search'])
                | Q(created__icontains=kwargs['search'])
                )[offset: offset+ limit]
    queryset = queryset[offset: offset+ limit]
    return queryset


@mutation.field("createOrder")
def resolve_create_order(obj, info, **kwargs):
    order = Order.objects.create(**kwargs)
    return order


@query.field("getOrder")
@convert_kwargs_to_snake_case
def resolve_get_order(obj, info, **kwargs):
    try:
        data_order = Order.objects.get(id=kwargs['id'])
    except Order.DoesNotExist:
        return None
    return data_order


@order.field("addHospital")
@convert_kwargs_to_snake_case
def resolve_add_demographics(obj, info, **kwargs):
    hospital = Hospital.objects.create(**kwargs)
    if hospital:
        data_order = Order.objects.get(id=obj.id)
        if data_order:
            data_order.hospital = hospital
            data_order.save()
        else:
            return False
    else:
        return False
    return True


@order.field("addPhysician")
# @convert_kwargs_to_snake_case
def resolve_add_physician(obj, info, **kwargs):
    physician = Physician.objects.create(**kwargs)
    if physician:
        data_order = Order.objects.get(id=obj.id)
        if data_order:
            data_order.physician = physician
            data_order.save()
        else:
            return False
    else:
        return False
    return True


@order.field("addSample")
def resolve_add_sample(obj, info, sampleId=None, patient=None):
    if not patient:
        return False
    patient = Patient.objects.create(
        firstName = patient['firstName'],
        middleName = patient['middleName'],
        address =  patient['address'],
        phoneNumber = patient['phoneNumber']
    )
    if not patient:
        return False

    new_sample = Sample.objects.create(
        sampleId = sampleId,
        patient = patient
        )
    if new_sample:
        data_order = Order.objects.get(id=obj.id)
        if data_order:
            data_order.sample = new_sample
            data_order.save()
        else:
            return False
    else:
        return False
    return True

resolvers = [query, mutation, order,]