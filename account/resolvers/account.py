"""Patients Resolvers """

from hospital.models import Hospital
from ariadne import convert_kwargs_to_snake_case
from ariadne import ObjectType, QueryType, MutationType
from django.db.models import Q
from ariadne_jwt.decorators import login_required
from lms_core import settings
from django.contrib.auth.models import User
from ariadne_jwt import resolve_verify, resolve_refresh, resolve_token_auth

query = QueryType()
mutation = MutationType()
account = ObjectType("User")

mutation.set_field('verifyToken', resolve_verify)
mutation.set_field('refreshToken', resolve_refresh)
mutation.set_field('tokenAuth', resolve_token_auth)

resolvers = [query, mutation, account, ]
