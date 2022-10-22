from itertools import count
from django.test import TestCase
from django.contrib.auth import get_user_model
from ariadne_jwt.testcases import JSONWebTokenTestCase

from schema import schema

class UserTests(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='dolphins')
        self.client.authenticate(self.user)
        self.client._schema =  schema

    def test_get_user(self):
            query = '''
            query GetPatient{
               patients{
                   id
               }
            }
            '''
            self.client.execute(query)
            assert len(query) > 0
