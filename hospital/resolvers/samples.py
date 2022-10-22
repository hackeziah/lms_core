""" Samples Resolvers """


from django.db.models import Q
from hospital.models import Sample
from datetime import date, datetime
from ariadne import convert_kwargs_to_snake_case
from ariadne import ObjectType, QueryType, MutationType

from lms_core import settings


query = QueryType()
mutation = MutationType()
sample = ObjectType("Sample")

@query.field("samples")
@convert_kwargs_to_snake_case
def resolve_samples(obj, info, **kwargs):
    offset = 0
    limit = settings.DEFAULT_LIMIT
    queryset = Sample.objects.all()

    if 'sort' in kwargs and 'order_by' in kwargs:
        if kwargs['sort'] == "ASC" and kwargs['order_by']:
            queryset = Sample.objects.all().order_by(kwargs['order_by'])
        elif kwargs['sort'] == "DESC" and kwargs['order_by']:
            queryset = Sample.objects.all().order_by('-'+kwargs['order_by'])
    else:
        queryset = Sample.objects.all()
    if queryset:
        if 'limit' in kwargs:
            limit = kwargs['limit']
        if 'offset' in kwargs:
            offset = kwargs['offset']
    if 'search' in kwargs:
        queryset = queryset.filter(
                Q(sampleId__icontains=kwargs['search'])
                | Q(patient__firstName__icontains=kwargs['search'])
                | Q(patient__lastName__icontains=kwargs['search'])
                | Q(patient__middleName__icontains=kwargs['search'])
                | Q(created__icontains=kwargs['search'])
            )[offset: offset+ limit]
    queryset = queryset[offset: offset+ limit]
    return queryset
    
@mutation.field("createSample")
def resolve_create_sample(obj, info, **kwargs):
    sample = Sample.objects.create(**kwargs)
    return sample


@mutation.field("deleteSample")
@convert_kwargs_to_snake_case
def resolve_delete_sample(obj, info, **kwargs):
    try:
        sample = Sample.objects.get(id=kwargs['id'])
        sample.isDeleted = True
        sample.save()
    except Sample.DoesNotExist:
        return False
    return True


@query.field("getSample")
@convert_kwargs_to_snake_case
def resolve_get_sample(obj, info, **kwargs):
    try:
        data_sample = Sample.objects.get(id=kwargs['id'])
    except Sample.DoesNotExist:
        return None
    return data_sample



@mutation.field("updateSample")
@convert_kwargs_to_snake_case
def resolve_update_sample(obj, info, **kwargs):
    try:
        sample = Sample.objects.get(id=kwargs['id'])
        sample.sampleId = kwargs['sampleId']
        sample.save()
    except Sample.DoesNotExist:
        return None
    return sample

@query.field("searchSample")
@convert_kwargs_to_snake_case
def resolve_search_sample(obj, info, **kwargs):
    try:
        samples = Sample.objects.filter(
                Q(sampleId__icontains=kwargs['search'])
                | Q(patient__firstName__icontains=kwargs['search'])
                | Q(patient__lastName__icontains=kwargs['search'])
                | Q(patient__middleName__icontains=kwargs['search'])
                | Q(created__icontains=kwargs['search'])
            )
    except Sample.DoesNotExist:
        return None
    return samples

resolvers = [query, mutation, sample,]
