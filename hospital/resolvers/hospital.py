"""Patients Resolvers """

from hospital.models import Hospital
from ariadne import convert_kwargs_to_snake_case
from ariadne import ObjectType, QueryType, MutationType
from django.db.models import Q
from ariadne_jwt.decorators import login_required
from lms_core import settings


query = QueryType()
mutation = MutationType()
hospital = ObjectType("Hospital")

"""Query Get All"""
@query.field("hospitals")
@convert_kwargs_to_snake_case
# @login_required
def resolve_hospitals(obj, info, **kwargs):
    """Field resolver for hospitals query.

    Args:
        obj: value returned by a parent resolver
        info: ResolverInfo, an instance of GraphQLResolveInfo.
              https://graphql.org/graphql-js/type/#graphqlobjecttype
        accession_issue_status_id: accession_issue_status id to query

    Returns:
        schema.Hospital
    """
    offset = 0
    limit = settings.DEFAULT_LIMIT
    queryset = Hospital.objects.all()

    if 'sort' in kwargs and 'order_by' in kwargs:
        if kwargs['sort']=="ASC" and kwargs['order_by']:
            queryset = Hospital.objects.all().order_by(kwargs['order_by'])
        elif kwargs['sort']=="DESC" and kwargs['order_by']:
            queryset = Hospital.objects.all().order_by('-'+kwargs['order_by'])
    else:
        queryset = Hospital.objects.all()
    if queryset:
        if 'limit' in kwargs:
            limit = kwargs['limit']
        if 'offset' in kwargs:
            offset = kwargs['offset']
    if 'search' in kwargs:
        queryset = queryset.filter(
                Q(name__icontains=kwargs['search'])
                | Q(address__icontains=kwargs['search'])
                | Q(created__icontains=kwargs['search'])
                )[offset: offset+ limit]
    queryset = queryset[offset: offset+ limit]
    return queryset


"""Query Get One Hospital"""

@query.field("getHospital")
@convert_kwargs_to_snake_case
def resolve_get_hospital(obj, info, **kwargs):
    """Field resolver for getHospital query.
    Args:
        obj: value returned by a parent resolver
        info: ResolverInfo, an instance of GraphQLResolveInfo.
              https://graphql.org/graphql-js/type/#graphqlobjecttype
        id: id to query
    Returns:
        schema.Hospital
    """
    try:
        hospital = Hospital.objects.get(id=kwargs['id'])
    except Hospital.DoesNotExist:
        return None
    return hospital



"""Mutation Create Hospital"""
@mutation.field("createHospital")
def resolve_create_hospital(obj, info, **kwargs):
    hospital = Hospital.objects.create(**kwargs)
    return hospital



@mutation.field("updateHospital")
@convert_kwargs_to_snake_case
def resolve_update_hospital(obj, info, **kwargs):
    try:
        hospital = Hospital.objects.get(id=kwargs['id'])
        hospital.name = kwargs['name']
        hospital.address = kwargs['address']
        hospital.save()
    except Hospital.DoesNotExist:
        return None
    return hospital


@mutation.field("deleteHospital")
@convert_kwargs_to_snake_case
def resolve_delete_hospital(obj, info, **kwargs):
    try:
        hospital = Hospital.objects.get(id=kwargs['id'])
        hospital.isDeleted = True
        hospital.save()
    except Hospital.DoesNotExist:
        return False
    return True


@query.field("searchHospital")
@convert_kwargs_to_snake_case
def resolve_search_hospitals(obj, info, **kwargs):
    try:
        hospitals = Hospital.objects.filter(
                Q(name__icontains=kwargs['search'])
                | Q(address__icontains=kwargs['search'])
                | Q(created__icontains=kwargs['search'])
            )
    except Hospital.DoesNotExist:
        return None
    return hospitals


resolvers = [query, mutation, hospital,]
