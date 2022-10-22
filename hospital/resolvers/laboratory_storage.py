""" Laboratory Storage Resolvers """


from multiprocessing.dummy import Array
from django.db.models import Q
from hospital.models import LaboratoryStorage
from datetime import date, datetime
from ariadne import convert_kwargs_to_snake_case
from ariadne import ObjectType, QueryType, MutationType

from lms_core import settings
from order.models import Order


query = QueryType()
mutation = MutationType()
laboratory_storage = ObjectType("LaboratoryStorage")


@query.field("laboratorystorage")
@convert_kwargs_to_snake_case
def resolve_laboratory_storage(obj, info, **kwargs):
    offset = 0
    limit = settings.DEFAULT_LIMIT
    queryset = LaboratoryStorage.objects.all()

    if 'sort' in kwargs and 'order_by' in kwargs:
        if kwargs['sort']=="ASC" and kwargs['order_by']:
            queryset = LaboratoryStorage.objects.all().order_by(kwargs['order_by'])
        elif kwargs['sort']=="DESC" and kwargs['order_by']:
            queryset = LaboratoryStorage.objects.all().order_by('-'+kwargs['order_by'])
    else:
        queryset = LaboratoryStorage.objects.all()
    if queryset:
        if 'limit' in kwargs:
            limit = kwargs['limit']
        if 'offset' in kwargs:
            offset = kwargs['offset']
    if 'search' in kwargs:
        queryset = queryset.filter(
                Q(name__icontains=kwargs['search'])
                | Q(location__icontains=kwargs['search'])
                # | Q(order__internalId__icontains=kwargs['search'])
                | Q(created__icontains=kwargs['search'])
                )[offset: offset+ limit]
    queryset = queryset[offset: offset+ limit]
    return queryset


@mutation.field("createLaboratoryStorage")
def resolve_create_laboratory_storage(obj, info, **kwargs):
    laboratory_storage = LaboratoryStorage.objects.create(**kwargs)
    return laboratory_storage


@mutation.field("deleteLaboratoryStorage")
@convert_kwargs_to_snake_case
def resolve_delete_LaboratoryStorage(obj, info, **kwargs):
    try:
        laboratory_storage = LaboratoryStorage.objects.get(id=kwargs['id'])
        laboratory_storage.isDeleted = True
        laboratory_storage.save()
    except LaboratoryStorage.DoesNotExist:
        return False
    return True


@query.field("getLaboratoryStorage")
@convert_kwargs_to_snake_case
def resolve_get_laboratory_storage(obj, info, **kwargs):
    try:
        laboratory_storage = LaboratoryStorage.objects.get(id=kwargs['id'])
    except LaboratoryStorage.DoesNotExist:
        return None
    return laboratory_storage



@mutation.field("updateLaboratoryStorage")
@convert_kwargs_to_snake_case
def resolve_update_laboratory_storage(obj, info, **kwargs):
    try:
        laboratory = LaboratoryStorage.objects.get(id=kwargs['id'])
        laboratory.name = kwargs['name']
        laboratory.location = kwargs['location']
        laboratory.save()

    except LaboratoryStorage.DoesNotExist:
        return None
    return laboratory


@query.field("searchLaboratoryStorage")
@convert_kwargs_to_snake_case
def resolve_search_laboratory(obj, info, **kwargs):
    try:
        lab_storage = LaboratoryStorage.objects.filter(
                Q(name__icontains=kwargs['search'])
                | Q(location__icontains=kwargs['search'])
                # | Q(order__internalId__icontains=kwargs['search'])
                | Q(created__icontains=kwargs['search'])
                )
    except LaboratoryStorage.DoesNotExist:
        return None
    return lab_storage

@laboratory_storage.field("addOrder")
def resolve_add_order_to_lab_storage(obj, info, **kwargs):
    try:
        laboratory = LaboratoryStorage.objects.get(id=obj.id)
    except LaboratoryStorage.DoesNotExist:
        return False

    try:
        order = Order.objects.get(id=kwargs['id'])
        order.status = "STORED"
        order.save()
    except Order.DoesNotExist:
        return False

    laboratory.orders.add(order)
    laboratory.save()
    return True


@laboratory_storage.field("addOrderList")
def resolve_add_order_to_lab_storage(obj, info, orderList=[]):
    try:
        laboratory = LaboratoryStorage.objects.get(id=obj.id)
    except LaboratoryStorage.DoesNotExist:
        return False
    if not orderList:
        return False
    for order_item in  orderList:
        try:
            order = Order.objects.get(id=order_item)
            order.status = "STORED"
            order.save()
        except Order.DoesNotExist:
            return False
        laboratory.orders.add(order)
        laboratory.save()
    return True


@laboratory_storage.field("removeOrderList")
def resolver_remover_order_item_to_lab_storage(obj, info, orderList=[]):
    try:
        laboratory = LaboratoryStorage.objects.get(id=obj.id)
    except LaboratoryStorage.DoesNotExist:
        return False
    if not orderList:
        return False
    for order_item in  orderList:
        try:
            order = Order.objects.get(id=order_item)
            order.status = "RECEIVED"
            order.save()
        except Order.DoesNotExist:
            return False
        laboratory.orders.remove(order)
        laboratory.save()
    return True

@laboratory_storage.field("orders")
def resolve_orders_to_lab_storage(obj, info):
    laboratory_storage = LaboratoryStorage.objects.get(id=obj.id)
    if not laboratory_storage:
        return []
    orders = laboratory_storage.orders.all()
    if not orders:
        return []
    return orders


resolvers = [query, mutation, laboratory_storage,]
