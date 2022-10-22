import os
from ariadne_jwt import jwt_schema, GenericScalar
from ariadne import gql, make_executable_schema, snake_case_fallback_resolvers, load_schema_from_path
from hospital.resolvers.patients import resolvers as patient_resolvers
from hospital.resolvers.hospital import resolvers as hospital_resolvers

from hospital.resolvers.physicians import resolvers as physicians_resolvers
from hospital.resolvers.samples import resolvers as sample_resolvers
from hospital.resolvers.laboratory_storage import resolvers as laboratory_storage_resolvers
from account.resolvers.account import resolvers as account_resolvers
from order.resolvers.orders import resolvers as orders_resolvers

bindables = []

bindables.extend(account_resolvers)
bindables.extend(patient_resolvers)
bindables.extend(hospital_resolvers)
bindables.extend(physicians_resolvers)
bindables.extend(sample_resolvers)
bindables.extend(laboratory_storage_resolvers)
bindables.extend(orders_resolvers)


type_defs = load_schema_from_path(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

schema = make_executable_schema(
    [type_defs +  jwt_schema],
    *bindables,
    GenericScalar
)