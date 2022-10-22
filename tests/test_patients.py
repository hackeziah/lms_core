""" Testing Patients Module."""

import imp
from ariadne import ObjectType, QueryType, graphql_sync, make_executable_schema
import pytest
from django.contrib.auth.models import User
from hospital.models import Patient
from hospital.resolvers import patients
from schema import schema as main_schema
from ariadne.contrib.federation import FederatedObjectType

def testing_example():
    assert 1 == 1


@pytest.mark.django_db
def test_user_create():
    """Testing """
    User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    assert User.objects.count() == 1



@pytest.fixture
def patient_001(db):
   patient, _ = Patient.objects.get_or_create(
       firstName='default',
       middleName="MIddle",
       lastName="Lastname",
       address="Taguig",
       phoneNumber ="02939239232"
       )
   return patient

# def testing_patients_all():
#     query = QueryType()
#     query.set_field("patients", patients)
#     schema = make_executable_schema(main_schema, query)
#     # chart = Chart.objects.create(....)
#     glquery = """ query{
#         patients{
#             id
#         }
#     }"""
#     result = graphql_sync(schema, glquery)
#     assert result.errors is None


def testing_resolver_patient(main_schema):
    obj = ObjectType("Patient")
    # obj.reference_resolver()(lambda *_: {"name": "Malbec"})
    schema = make_executable_schema(main_schema, query)
    obj.bind_to_schema(schema)

    result = graphql_sync(
        schema,
        """
           query{
            patients{
                id
           }
        """
    )

    assert result.errors is None
    assert len( result.data["patients"]) == 1