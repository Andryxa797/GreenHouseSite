from django.test import TestCase, Client
from rest_framework.authtoken.admin import User

from house.forms import UserSetting, NewSignerForm
from house.models import Profile, Signer, DataHouse


class ModelORMTestCase(TestCase):

    def create_user_data(self):
        self.owner = User.objects.create(username="Owner", first_name='Andrey', password="2222")
        self.owner.save()
        Profile.objects.filter(pk=self.owner.id).update(user_is_microcontroller=True)
        self.user = User.objects.create(username="User", password="2222")
        self.SingerObj = Signer.objects.create(user=self.user, owner_name=self.owner, published=True, on_check=True)
        self.Data = DataHouse.objects.create(
            temp_greenhouse_upstairs=25,
            temp_greenhouse_downstairs=25,
            temp_greenhouse_in_ground=25,
            temp_street=25,
            humidity_greenhouse=25,
            humidity_greenhouse_in_ground=25,
            servo_turn_upstairs=180,
            servo_turn_downstairs=0,
            conditions_load_one=False,
            conditions_load_two=True,
            conditions_load_three=True,
            owner=User.objects.get(pk=self.owner.pk)
        )

    def test_create_user(self):
        self.user = User.objects.create(username="Andrey", password="2222")
        self.user = User.objects.create(username="Dima", password="2222")
        self.user_is_micro = User.objects.create(username="Ivan", password="2222")
        self.user.save()
        form = UserSetting(data={"email": "andrey@mail.ru", "first_name": "da"})
        print(form.is_valid())
        form = UserSetting(data={"email": "andrey@mail.ru", "first_name": "da", "last_name": "da" })
        print(form.is_valid())
        self.assertTrue(form.is_valid())

    def test_create_user(self):
        # form = NewSignerForm(data={"user": "andrey", "owner_name": "Andrey", "published": True, "on_check": False })
        form = NewSignerForm(data={"owner_name": "Andrey"})
        self.assertTrue(form.is_valid())

