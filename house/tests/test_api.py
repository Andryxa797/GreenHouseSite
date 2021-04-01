from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class DataHouseApiTestCase(APITestCase):

    def CreateUserAndToken(self):
        self.user = User.objects.create(username="Andrey", password="2222")
        self.user.save()
        self.token = Token.objects.create(key='d4ecde5c54cc87a6e38f360a9fff3dae2976fd8f', user=self.user)
        self.token.save()

    def test_data_before_process_get_data(self):
        self.CreateUserAndToken()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'd4ecde5c54cc87a6e38f360a9fff3dae2976fd8f')
        request = self.client.get('/api-data/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_data_before_process_post_data(self):
        self.CreateUserAndToken()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'd4ecde5c54cc87a6e38f360a9fff3dae2976fd8f')
        request = self.client.post('/api-data/', {
            "temp_greenhouse_upstairs": "25",
            "temp_greenhouse_downstairs": "25",
            "temp_greenhouse_in_ground": "30",
            "temp_street": "20",
            "humidity_greenhouse": "60",
            "humidity_greenhouse_in_ground": "80",
            "servo_turn_upstairs": "90",
            "servo_turn_downstairs": "180",
            "conditions_load_one": True,
            "conditions_load_two": False,
            "conditions_load_three": False
        }, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
