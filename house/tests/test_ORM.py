from django.test import TestCase, Client
from rest_framework.authtoken.admin import User

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
        Profile.objects.filter(pk=self.user_is_micro.id).update(user_is_microcontroller=True)
        profiles = Profile.objects.all().filter(user_is_microcontroller=True)
        name = ''
        for profile in profiles:
            name = profile.user
        self.assertEqual(name, Profile.objects.get(pk=self.user_is_micro.id).user)

    def test_get_singer(self):
        self.create_user_data()
        owners = Signer.objects.filter(user=self.user.pk)
        owner_data = []
        for owner in owners:
            owner_data.append(User.objects.get(pk=owner.pk).first_name)
        print(owner_data)

    def test_get_avatar(self):
        self.create_user_data()
        owners = Signer.objects.filter(user=self.user.pk)
        owner_first_name = []
        owner_username = []
        owner_avatar = []
        for owner in owners:
            owner_username.append(User.objects.get(pk=owner.pk).username)
            owner_first_name.append(User.objects.get(pk=owner.pk).first_name)
            owner_avatar = Profile.objects.get(pk=owner.pk).avatar
        print(owner_username)
        print(owner_first_name)
        print(owner_avatar)

    def test_get_signer(self):
        self.create_user_data()
        owners1 = Profile.objects.filter(user_is_microcontroller=True).values_list('user__username', flat=True)
        print(owners1)
        owners2 = Signer.objects.filter(user=self.user).values_list(
            'user__username', flat=True)
        print(owners2)
