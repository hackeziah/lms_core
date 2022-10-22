import imp
from itertools import count
import re
from schema import schema
from this import s
from unicodedata import name
from django.test import TestCase
from django.contrib.auth import get_user_model
from ariadne_jwt.testcases import JSONWebTokenTestCase
from graphql import Location
from hospital.models import *


class HopitalTests(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='dolphins')
        self.client.authenticate(self.user)
        self.client._schema =  schema
        self.hospital_1 = Hospital.objects.create(
            name="Makati Hospital",
            address= "Address Makati"
        )

        self.hospital_2 = Hospital.objects.create(
            name="ST. Luke Hospital",
            address= "Address Taguig"
        )


        self.physicians_1 = Physician.objects.create(
            firstName="Kevin",
            middleName="Acilla",
            lastName="Lamadrid",
            address= "Taguig",
            phoneNumber="09239239232"
        )

        self.physicians_2 = Physician.objects.create(
            firstName="Juan",
            middleName="Dela",
            lastName="Cruz",
            address= "Taguig",
            phoneNumber="092392123211"
        )

        self.patient_1 = Patient.objects.create(
            firstName="Patient 01",
            middleName="Acilla",
            lastName="Lamadrid",
            address= "Taguig",
            phoneNumber="09239239232"
        )

        self.patient_2 = Patient.objects.create(
            firstName="Patient 02",
            middleName="Dela",
            lastName="Cruz",
            address= "Taguig",
            phoneNumber="092392123211"
        )

        self.lab_storage_1 = LaboratoryStorage.objects.create(
             name = "LAB 101",
             location =  "Taguig"
        )

        
        self.lab_storage_2 = LaboratoryStorage.objects.create(
             name = "LAB 102",
             location =  "Manila City"
        )


        self.sample_1 = Sample.objects.create(
             sampleId = "SAMPLE TEST 01",
             patient = self.patient_1
        )

        
        self.sample_2 = Sample.objects.create(
             sampleId  = "SAMPLE TEST 02",
             patient = self.patient_2
        )
        
# ///HOSPITAL TEST
    def test_get_hospital(self):
        query = '''
        query getDataHospital($id: ID!) {
            getHospital(id: $id) {
                id
                name
                address
            }
        }
        '''

        results = self.client.execute(query, variables={
            "id": str(self.hospital_1.id)
        })
        ros = results.data["getHospital"]
        assert ros["id"] == str(self.hospital_1.id)
        assert ros["name"] == "Makati Hospital"
        assert ros["address"] == "Address Makati"

    def test_get_all_hospitals(self):
        query = '''
        query getDataHospital{
            hospitals{
                id
                name
                address
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["hospitals"]
        assert len(data) == 2

    def test_delete_hospital(self):
        query = '''
        query getDataHospital{
            hospitals{
                id
                name
                address
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["hospitals"]
        assert len(data) == 2

        query = '''
        mutation deleteHospital($id: ID!) {
            deleteHospital(id: $id)
        }
        '''
        results = self.client.execute(query, variables={
            "id": str(self.hospital_1.id)
        })
        assert results.data["deleteHospital"]

        query = '''
        query getAllHospitasl{
            hospitals{
                id
                name
                address
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["hospitals"]
        assert len(data) == 1

    # updateHospital
    def test_update_hospital(self):
        query = '''
        mutation updateHospital($id: ID!, $name: String!, $address: String!) {
            updateHospital(id: $id, name: $name, address: $address ){
                name
                address
            }
        }
        '''
        results = self.client.execute(query, variables={
            "id": str(self.hospital_1.id),
            "name": "Sample",
            "address": "Sample New"
        })
        assert results.data["updateHospital"]


        query = '''
        query getHospital1($id: ID!) {
            getHospital(id: $id){
                name
                address
            }
        }
        '''
        results = self.client.execute(query, variables={
            "id": str(self.hospital_1.id)
        })
        data = results.data["getHospital"]
        assert  data['name'] == "Sample"
        assert  data['address'] == "Sample New"

    def test_create_hospital(self):
        query = '''
        query getAllHospitasl{
            hospitals{
                id
                name
                address
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["hospitals"]
        assert len(data) == 2
        
        query = '''
        mutation createHospitalData( $name: String!, $address: String!){
            createHospital(name: $name, address: $address){
                name
                address
            }
        }
        '''

        results = self.client.execute(query, variables={
            "name": "Taguig Hospital",
            "address": "Taguig",
        })
        assert results.data["createHospital"]

        query = '''
        query getAllHospitasl{
            hospitals{
                id
                name
                address
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["hospitals"]
        assert len(data) == 3
    
    def test_search_hospital(self):
        query = '''
        query searchHospital($search: String ){
            hospitals(search: $search){
                name
                address
            }
        }
        '''

        results = self.client.execute(query, variables={
            "search": "Luke",
        })
        assert results.data["hospitals"]
        data = results.data["hospitals"]
        assert data[0]['name'] == "ST. Luke Hospital"
        
# /////HOSPITAL TEST
# /////PHYSICIAN TEST
    def test_get_all_physicians(self):
        query = '''
        query getAllPhysicians{
            physicians{
                id
                firstName
                middleName
                lastName
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["physicians"]
        assert len(data) == 2
        assert data[0]['lastName'] == "Lamadrid"
        assert data[1]['lastName'] == "Cruz"

    def test_get_one_physicians(self):
        query = '''
        query getPhysicianOne($id : ID!){
            getPhysician(id: $id){
                id
                firstName
                middleName
                lastName
            }
        }
        '''

        results = self.client.execute(query, variables = {
            'id': str(self.physicians_1.id)
        })
        data = results.data["getPhysician"]
        assert results.data["getPhysician"]
        assert data['id'] == str(self.physicians_1.id)
        assert data['lastName'] == "Lamadrid"
        assert data['firstName'] == "Kevin"

    def test_get_update_physicians(self):
        query = '''
        query getPhysicianOne($id : ID!){
            getPhysician(id: $id){
                id
                firstName
                middleName
                lastName
            }
        }
        '''

        results = self.client.execute(query, variables = {
            'id': str(self.physicians_1.id)
        })
        data = results.data["getPhysician"]
        assert results.data["getPhysician"]
        assert data['id'] == str(self.physicians_1.id)
        assert data['lastName'] == "Lamadrid"
        assert data['firstName'] == "Kevin"

        query = '''
        mutation updatePhysicianOne($id: ID!, $firstName: String!, $middleName: String, $lastName: String!, $address: String!, $phoneNumber: String){
            updatePhysician(id: $id, firstName: $firstName, middleName: $middleName, lastName: $lastName, address: $address, phoneNumber: $phoneNumber){
                id
                firstName
                middleName
                lastName
                address
                phoneNumber
            }
        }
        '''

        results = self.client.execute(query, variables = {
            'id': str(self.physicians_1.id),
            'firstName': "Paul",
            'middleName': "Cruz",
            'lastName': "Cruz",
            'address': "Makati Update",
            'phoneNumber': "0981717171",

        })
        assert results.data["updatePhysician"]
        data = results.data["updatePhysician"]
        assert data['id'] == str(self.physicians_1.id)
        assert data['lastName'] == "Cruz"
        assert data['firstName'] == "Paul"


    def test_create_delete_physician(self):
        query = '''
        query getAllPhysicians{
            physicians{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["physicians"]
        assert len(data) == 2

        query = '''
        mutation createPhysician($firstName: String!, $middleName: String, $lastName: String!, $address: String!, $phoneNumber: String){
            createPhysician( firstName: $firstName, middleName: $middleName, lastName: $lastName, address: $address, phoneNumber: $phoneNumber){
                id
                firstName
                middleName
                lastName
                address
                phoneNumber
            }
        }
        '''
        results = self.client.execute(query, variables = {
            'firstName': "Jose",
            'middleName': "Cruz",
            'lastName': "Rizal",
            'address': "Makati Added",
            'phoneNumber': "092322333",

        })
        assert results.data["createPhysician"]

        query = '''
        query getAllPhysicians{
            physicians{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["physicians"]
        assert len(data) == 3

        query = '''
        mutation deletePhysicianOne($id : ID!){
            deletePhysician(id: $id)
        }
        '''

        results = self.client.execute(query, variables = {
            'id': str(self.physicians_1.id)
        })
        assert results.data["deletePhysician"]

        query = '''
        query getAllPhysicians{
            physicians{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["physicians"]
        assert len(data) == 2

    def test_search_physician(self):
        query = '''
        query getAllPhysicians{
            physicians{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["physicians"]
        assert len(data) == 2

        query = '''
        query getPhysicianOne($id : ID!){
            getPhysician(id: $id){
                id
                firstName
                middleName
                lastName
            }
        }
        '''

        results = self.client.execute(query, variables = {
            'id': str(self.physicians_1.id)
        })
        data = results.data["getPhysician"]
        assert results.data["getPhysician"]
        assert data['id'] == str(self.physicians_1.id)
        assert data['lastName'] == "Lamadrid"
        assert data['firstName'] == "Kevin"
           
        query = '''
        query searchPhysicians($search: String ){
            physicians(search: $search){
                firstName
                middleName
                lastName
            }
        }
        '''

        results = self.client.execute(query, variables={
            "search": "Lamad",
        })

        assert results.data["physicians"]
        assert data['id'] == str(self.physicians_1.id)
        assert data['lastName'] == "Lamadrid"
        assert data['firstName'] != "Juan"

# /////PHYSICIAN TEST
# /////PATIENTS TEST
    def test_get_all_patients(self):
        query = '''
        query getAllPhysicians{
            patients{
                id
                firstName
                middleName
                lastName
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["patients"]
        assert len(data) == 2
        assert data[0]['lastName'] == "Lamadrid"
        assert data[1]['lastName'] == "Cruz"

    def test_get_one_patient(self):
        query = '''
        query getPatientOne($id : ID!){
            getPatient(id: $id){
                id
                firstName
                middleName
                lastName
            }
        }
        '''

        results = self.client.execute(query, variables = {
            'id': str(self.patient_1.id)
        })
        data = results.data["getPatient"]
        assert results.data["getPatient"]
        assert data['id'] == str(self.patient_1.id)
        assert data['lastName'] == "Lamadrid"
        assert data['firstName'] == "Patient 01"

    def test_get_update_patients(self):
        query = '''
        query getPatientOne($id : ID!){
            getPatient(id: $id){
                id
                firstName
                middleName
                lastName
            }
        }
        '''

        results = self.client.execute(query, variables = {
            'id': str(self.patient_2.id)
        })
        data = results.data["getPatient"]
        assert results.data["getPatient"]
        assert data['id'] == str(self.patient_2.id)
        assert data['lastName'] == "Cruz"
        assert data['firstName'] == "Patient 02"

        query = '''
        mutation updatePatientOne($id: ID!, $firstName: String!, $middleName: String, $lastName: String!, $address: String!, $phoneNumber: String){
            updatePatient(id: $id, firstName: $firstName, middleName: $middleName, lastName: $lastName, address: $address, phoneNumber: $phoneNumber){
                id
                firstName
                middleName
                lastName
                address
                phoneNumber
            }
        }
        '''

        results = self.client.execute(query, variables = {
            'id': str(self.patient_2.id),
            'firstName': "Paul",
            'middleName': "Cruz",
            'lastName': "Cruz",
            'address': "Makati New Update",
            'phoneNumber': "09955513239",

        })
        assert results.data["updatePatient"]
        data = results.data["updatePatient"]
        assert data['id'] == str(self.patient_2.id)
        assert data['lastName'] == "Cruz"
        assert data['firstName'] == "Paul"
        assert data['phoneNumber'] == "09955513239"

    def test_create_delete_patient(self):
        query = '''
        query getAllPhysicians{
            patients{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["patients"]
        assert len(data) == 2

        query = '''
        mutation createPatient($firstName: String!, $middleName: String, $lastName: String!, $address: String!, $phoneNumber: String){
            createPatient(firstName: $firstName, middleName: $middleName, lastName: $lastName, address: $address, phoneNumber: $phoneNumber){
                id
                firstName
                middleName
                lastName
                address
                phoneNumber
            }
        }
        '''
        results = self.client.execute(query, variables = {
            'firstName': "Joseph",
            'middleName': "Cruz",
            'lastName': "Rizal",
            'address': "Quezon City Added",
            'phoneNumber': "0929282828249",

        })
        assert results.data["createPatient"]

        query = '''
        query getAllPatients{
            patients{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["patients"]
        assert len(data) == 3

        query = '''
        mutation deletePatientOne($id : ID!){
            deletePatient(id: $id)
        }
        '''

        results = self.client.execute(query, variables = {
            'id': str(self.patient_1.id)
        })
        assert results.data["deletePatient"]

        query = '''
        query getAllPhysicians{
            patients{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["patients"]
        assert len(data) == 2

    def test_search_patients(self):
        query = '''
        query getAllPatients{
            patients{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["patients"]
        assert len(data) == 2

        query = '''
        query getPatientOne($id : ID!){
            getPatient(id: $id){
                id
                firstName
                middleName
                lastName
                phoneNumber
            }
        }
        '''

        results = self.client.execute(query, variables = {
            'id': str(self.patient_1.id)
        })
        data = results.data["getPatient"]
        assert results.data["getPatient"]
        assert data['id'] == str(self.patient_1.id)
        assert data['lastName'] == "Lamadrid"
        assert data['firstName'] == "Patient 01"
        assert data['phoneNumber'] == "09239239232"

        query = '''
        query searchPhysicians($search: String ){
            patients(search: $search){
                firstName
                middleName
                lastName
                phoneNumber
            }
        }
        '''

        results = self.client.execute(query, variables={
            "search": "Patient 0",
        })

        assert results.data["patients"]
        assert data['id'] == str(self.patient_1.id)
        assert data['lastName'] == "Lamadrid"
        assert data['firstName'] == "Patient 01"
        assert data['phoneNumber'] == "09239239232"

# /////LABORATORY STORAGE TEST

    def test_get_lab_storage(self):
        query = '''
        query getLaboratoryStorage($id: ID!) {
            getLaboratoryStorage(id: $id) {
                id
                name
                location
            }
        }
        '''

        results = self.client.execute(query, variables={
            "id": str(self.lab_storage_1.id)
        })
        ros = results.data["getLaboratoryStorage"]
        assert ros["id"] == str(self.lab_storage_1.id)
        assert ros["name"] ==  "LAB 101"
        assert ros["location"] == "Taguig"

    def test_get_all_laboratories(self):
        query = '''
        query getLabs{
            laboratorystorage{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["laboratorystorage"]
        assert len(data) == 2

    def test_delete_one_lab(self):
        query = '''
        query getLabs{
            laboratorystorage{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["laboratorystorage"]
        assert len(data) == 2

        query = '''
        mutation deleteOneLab($id: ID!) {
            deleteLaboratoryStorage(id: $id)
        }
        '''
        results = self.client.execute(query, variables={
            "id": str(self.lab_storage_1.id)
        })
        assert results.data["deleteLaboratoryStorage"]

        query = '''
        query getAllLabs{
            laboratorystorage{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["laboratorystorage"]
        assert len(data) == 1

    # updateLabStorage
    def test_update_lab(self):
        query = '''
        query getLaboratoryStorageOne($id: ID!) {
            getLaboratoryStorage(id: $id){
                name
                location
            }
        }
        '''
        results = self.client.execute(query, variables={
            "id": str(self.lab_storage_1.id)
        })
        data = results.data["getLaboratoryStorage"]
        assert  data['name'] == "LAB 101"
        assert  data['location'] == "Taguig"

        query = '''
        mutation updateLaboratoryStorage($id: ID!, $name: String!, $location: String!) {
            updateLaboratoryStorage(id: $id, name: $name, location: $location ){
                id
                name
                location
            }
        }
        '''
        results = self.client.execute(query, variables={
            "id": str(self.lab_storage_1.id),
            "name": "LAB 0101",
            "location": "Sample New"
        })
        assert results.data["updateLaboratoryStorage"]   
        data = results.data["updateLaboratoryStorage"]
        assert data['id'] ==  str(self.lab_storage_1.id)
        assert data['name'] ==  "LAB 0101"

    def test_create_lab(self):
        query = '''
        query getAllLaboratoryStorage{
            laboratorystorage{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["laboratorystorage"]
        assert len(data) == 2
        
        query = '''
        mutation createLabData( $name: String!, $location: String!){
            createLaboratoryStorage(name: $name, location: $location){
                name
                location
            }
        }
        '''

        results = self.client.execute(query, variables={
            "name": "Taguig Laboratory Storage",
            "location": "Taguig",
        })
        assert results.data["createLaboratoryStorage"]

        query = '''
        query getAllLaboratoryStorage{
            laboratorystorage{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["laboratorystorage"]
        assert len(data) == 3
    
    def test_search_lab(self):
        query = '''
        query searchLab($search: String ){
            laboratorystorage(search: $search){
                name
                location
            }
        }
        '''

        results = self.client.execute(query, variables={
            "search": "LAB 102",
        })
        assert results.data["laboratorystorage"]
        data = results.data["laboratorystorage"]
        assert data[0]['name'] == "LAB 102"
        assert data[0]['location'] != "ST. Luke Hospital"


#SAMPLE LABORATORY
    def test_get_sample(self):
        query = '''
        query getSampleOne($id: ID!) {
            getSample(id: $id) {
                id
            }
        }
        '''

        results = self.client.execute(query, variables={
            "id": str(self.sample_1.id)
        })
        data = results.data["getSample"]
        assert data["id"] == str(self.sample_1.id)

    def test_get_all_samples(self):
        query = '''
        query getSamples{
            samples{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["samples"]
        assert len(data) == 2

    def test_delete_one_samples(self):
        query = '''
        query getSamples{
            samples{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["samples"]
        assert len(data) == 2

        query = '''
        mutation deleteOneSample($id: ID!) {
            deleteSample(id: $id)
        }
        '''
        results = self.client.execute(query, variables={
            "id": str(self.sample_1.id)
        })
        assert results.data["deleteSample"]

        query = '''
        query getAllLabs{
            samples{
                id
            }
        }
        '''

        results = self.client.execute(query)
        data = results.data["samples"]
        assert len(data) == 1

    # # updateLabStorage
    # def test_update_lab(self):
    #     query = '''
    #     query getLaboratoryStorageOne($id: ID!) {
    #         getLaboratoryStorage(id: $id){
    #             name
    #             location
    #         }
    #     }
    #     '''
    #     results = self.client.execute(query, variables={
    #         "id": str(self.lab_storage_1.id)
    #     })
    #     data = results.data["getLaboratoryStorage"]
    #     assert  data['name'] == "LAB 101"
    #     assert  data['location'] == "Taguig"

    #     query = '''
    #     mutation updateLaboratoryStorage($id: ID!, $name: String!, $location: String!) {
    #         updateLaboratoryStorage(id: $id, name: $name, location: $location ){
    #             id
    #             name
    #             location
    #         }
    #     }
    #     '''
    #     results = self.client.execute(query, variables={
    #         "id": str(self.lab_storage_1.id),
    #         "name": "LAB 0101",
    #         "location": "Sample New"
    #     })
    #     assert results.data["updateLaboratoryStorage"]   
    #     data = results.data["updateLaboratoryStorage"]
    #     assert data['id'] ==  str(self.lab_storage_1.id)
    #     assert data['name'] ==  "LAB 0101"

    # def test_create_lab(self):
    #     query = '''
    #     query getAllLaboratoryStorage{
    #         laboratorystorage{
    #             id
    #         }
    #     }
    #     '''

    #     results = self.client.execute(query)
    #     data = results.data["laboratorystorage"]
    #     assert len(data) == 2
        
    #     query = '''
    #     mutation createLabData( $name: String!, $location: String!){
    #         createLaboratoryStorage(name: $name, location: $location){
    #             name
    #             location
    #         }
    #     }
    #     '''

    #     results = self.client.execute(query, variables={
    #         "name": "Taguig Laboratory Storage",
    #         "location": "Taguig",
    #     })
    #     assert results.data["createLaboratoryStorage"]

    #     query = '''
    #     query getAllLaboratoryStorage{
    #         laboratorystorage{
    #             id
    #         }
    #     }
    #     '''

    #     results = self.client.execute(query)
    #     data = results.data["laboratorystorage"]
    #     assert len(data) == 3
    
    # def test_search_lab(self):
    #     query = '''
    #     query searchLab($search: String ){
    #         laboratorystorage(search: $search){
    #             name
    #             location
    #         }
    #     }
    #     '''
    #     results = self.client.execute(query, variables={
    #         "search": "LAB 102",
    #     })
    #     assert results.data["laboratorystorage"]
    #     data = results.data["laboratorystorage"]
    #     assert data[0]['name'] == "LAB 102"
    #     assert data[0]['location'] != "ST. Luke Hospital"
