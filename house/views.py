from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from house.forms import UserLoginForm, UserRegisterForm, UserSetting, UserContact, NewSignerAgreeForm, NewSignerForm
from house.models import DataHouse, Signer, Profile
from house.permissions import ReadOnly, IsOwnerOrReadOnlyForAuthenticated
from house.serializers import DataHouseSerializer, OwnerSerializer


class DataHouseViewSet(viewsets.ModelViewSet):
    queryset = DataHouse.objects.get_queryset().order_by('id')
    serializer_class = DataHouseSerializer
    permission_classes = [IsOwnerOrReadOnlyForAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            owner_search = Signer.objects.filter(user=self.request.user, published=True)
            owner = []
            for item in owner_search:
                owner.append(item.owner_name)
                try:
                    if str(item.owner_name) == self.kwargs['owner']:
                        print(self.kwargs['owner'])
                        return DataHouse.objects.filter(owner__username=self.kwargs['owner'])
                except:
                    return DataHouse.objects.none()
        else:
            return DataHouse.objects.none()


class OwnerViewSet(ModelViewSet):
    queryset = Signer.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [ReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        owner_name = Signer.objects.filter(user=self.request.user, published=True)
        return owner_name


class HomeView(ListView):
    template_name = 'house/home_list.html'
    context_object_name = 'data'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            owners = Signer.objects.filter(user=self.request.user.pk)
            owner_username = []
            owner_first_name = []
            owner_avatar = []
            for owner in owners:
                get_owner = User.objects.get(username=owner.owner_name)
                owner_username.append(get_owner.username)
                owner_first_name.append(get_owner.first_name)
                owner_avatar.append(get_owner.profile.avatar.url)
            context['range'] = range(len(owner_username))
            context['OwnerUserName'] = owner_username
            context['OwnerFirstName'] = owner_first_name
            context['PathImg'] = owner_avatar
        return context


class DataView(ListView):
    template_name = 'house/data_detail.html'
    queryset = DataHouse

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            owners = Signer.objects.filter(user=self.request.user.pk)
            data = []
            owner_username = []
            owner_first_name = []
            owner_avatar = []
            labels = []
            temp_greenhouse_upstairs = []
            temp_greenhouse_downstairs = []
            temp_greenhouse_in_ground = []
            temp_street = []
            humidity_greenhouse = []
            humidity_greenhouse_in_ground = []
            servo_turn_upstairs = []
            servo_turn_downstairs = []
            conditions_load_one = []
            conditions_load_two = []
            conditions_load_three = []
            count = 0
            for owner in owners:
                if str(owner.owner_name) == self.kwargs['owner_name']:
                    data = DataHouse.objects.filter(owner__username=owner.owner_name)[:self.kwargs['count_value_chart']]
                    get_owner = User.objects.get(username=owner.owner_name)
                    owner_username.append(get_owner.username)
                    owner_first_name.append(get_owner.first_name)
                    owner_avatar.append(get_owner.profile.avatar.url)
                    for item in data:
                        temp_greenhouse_upstairs.append(item.temp_greenhouse_upstairs)
                        temp_greenhouse_downstairs.append(item.temp_greenhouse_downstairs)
                        temp_greenhouse_in_ground.append(item.temp_greenhouse_in_ground)
                        temp_street.append(item.temp_street)
                        humidity_greenhouse.append(item.humidity_greenhouse)
                        humidity_greenhouse_in_ground.append(item.humidity_greenhouse_in_ground)
                        servo_turn_upstairs.append(item.servo_turn_upstairs)
                        servo_turn_downstairs.append(item.servo_turn_downstairs)
                        conditions_load_one.append(int(item.conditions_load_one))
                        conditions_load_two.append(int(item.conditions_load_two))
                        conditions_load_three.append(int(item.conditions_load_three))
                        labels.append(count)
                        count += 1
            context['Data'] = data
            context['OwnerUserName'] = owner_username
            context['OwnerFirstName'] = owner_first_name
            context['PathImg'] = owner_avatar
            context['labels'] = labels
            context['temp_greenhouse_upstairs'] = temp_greenhouse_upstairs
            context['temp_greenhouse_downstairs'] = temp_greenhouse_downstairs
            context['temp_greenhouse_in_ground'] = temp_greenhouse_in_ground
            context['temp_street'] = temp_street
            context['humidity_greenhouse'] = humidity_greenhouse
            context['humidity_greenhouse_in_ground'] = humidity_greenhouse_in_ground
            context['servo_turn_upstairs'] = servo_turn_upstairs
            context['servo_turn_downstairs'] = servo_turn_downstairs
            context['conditions_load_one'] = conditions_load_one
            context['conditions_load_two'] = conditions_load_two
            context['conditions_load_three'] = conditions_load_three
        return context


class DataTableView(ListView):
    template_name = 'house/data_table_detail.html'
    queryset = DataHouse
    paginate_by = 100
    context_object_name = 'data'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            owners = Signer.objects.filter(user=self.request.user.pk)
            for owner in owners:
                if str(owner.owner_name) == self.kwargs['owner_name']:
                    data = DataHouse.objects.filter(owner__username=owner.owner_name)
                    if data is not None:
                        return data
                    if data is None:
                        return DataHouse.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            owners = Signer.objects.filter(user=self.request.user.pk)
            owner_username = []
            owner_first_name = []
            for owner in owners:
                if str(owner.owner_name) == self.kwargs['owner_name']:
                    get_owner = User.objects.get(username=owner.owner_name)
                    owner_username.append(get_owner.username)
                    owner_first_name.append(get_owner.first_name)
            context['OwnerUserName'] = owner_username
            context['OwnerFirstName'] = owner_first_name
            context['Category'] = self.kwargs['category']
        return context


def lk_view(request):
    if request.method == 'POST' and 'ButtonChangeUserSetting' in request.POST:
        if request.user.is_authenticated:
            user_setting_form = UserSetting(data=request.POST)
            if user_setting_form.is_valid():
                first_name = user_setting_form.cleaned_data['first_name']
                last_name = user_setting_form.cleaned_data['last_name']
                email = user_setting_form.cleaned_data['email']
                User.objects.filter(pk=request.user.pk).update(first_name=first_name, last_name=last_name, email=email)
                path_img = User.objects.get(pk=request.user.pk).profile.avatar.url
                return redirect('lk')
    elif request.method == 'POST' and 'ButtonChangeContact' in request.POST:
        if request.user.is_authenticated:
            user_contact_form = UserContact(data=request.POST)
            print(user_contact_form.is_valid())
            if user_contact_form.is_valid():
                address = user_contact_form.cleaned_data['address']
                number_telephone = user_contact_form.cleaned_data['number_telephone']
                city = user_contact_form.cleaned_data['city']
                country = user_contact_form.cleaned_data['country']
                Profile.objects.filter(user=request.user).update(address=address, number_telephone=number_telephone,
                                                                 city=city, country=country)
                return redirect('lk')
    elif request.method == 'POST' and 'UploadAvatar' in request.POST:
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            profile.avatar.delete()
            profile.avatar = request.FILES["image"]
            profile.save()
            return redirect('lk')

    else:
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            user_setting_form = UserSetting(
                initial={"first_name": user.first_name, "last_name": user.last_name, "email": user.email})
            user_contact_form = UserContact(
                initial={"address": user.profile.address, "number_telephone": user.profile.number_telephone,
                         "city": user.profile.city, "country": user.profile.country})
            path_img = User.objects.get(pk=request.user.pk).profile.avatar.url
            return render(request, 'house/lk.html',
                          {"user_setting_form": user_setting_form,
                           "user_contact_form": user_contact_form,
                           "path_img": path_img,
                           })


def followers_view(request):
    if request.method == 'POST' and 'AddSigner' in request.POST:
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            if user.profile.user_is_microcontroller is True:
                owner_answer_add = Signer(owner_name=request.user, published=True, on_check=True)
                owner_answer_add = NewSignerAgreeForm(request.POST, instance=owner_answer_add)
                if owner_answer_add.is_valid():
                    print('valid')
                    owner_answer_add.save()
                    return redirect('lk')
                return redirect('lk')
    if request.method == 'POST' and 'RemoveSigner' in request.POST:
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            if user.profile.user_is_microcontroller is True:
                owner_answer_remove = NewSignerAgreeForm(request.POST)
                if owner_answer_remove.is_valid():
                    obj = Signer.objects.filter(owner_name=request.user, user=owner_answer_remove.cleaned_data['user'])
                    obj.delete()
                    return redirect('followers')
                return redirect('followers')
    if request.method == 'POST' and 'AddOwner' in request.POST:
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            if user.profile.user_is_microcontroller is False:
                user_name = Signer(user=request.user)
                add_owner = NewSignerAgreeForm(request.POST, instance=user_name)
                print(add_owner.is_valid())
                if add_owner.is_valid():
                    add_owner.save()
                    return redirect('followers')
                return redirect('followers')
    if request.method == 'POST' and 'RemoveOwner' in request.POST:
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            if user.profile.user_is_microcontroller is False:
                remove_owner = NewSignerForm(request.POST)
                print(remove_owner.is_valid())
                if remove_owner.is_valid():
                    obj = Signer.objects.filter(owner_name=request.user, user=remove_owner.cleaned_data['owner_name'])
                    obj.delete()
                    return redirect('followers')
                return redirect('followers')

    if request.method == 'GET':
        if request.user.is_authenticated:
            is_microcontroller = False
            user = User.objects.get(pk=request.user.pk)
            if user.profile.user_is_microcontroller is True:
                is_microcontroller = True
                agree_form = NewSignerAgreeForm()
                signer = Signer.objects.filter(owner_name=request.user, published=True)
                agree_form.fields['user'].queryset = User.objects.filter(user__owner_name=request.user,
                                                                         user__on_check=False)
                disagree_form = NewSignerAgreeForm()
                disagree_form.fields['user'].queryset = User.objects.filter(user__owner_name=request.user,
                                                                            user__on_check=True,
                                                                            user__published=True)
                return render(request, 'house/followers.html',
                              {'agree_form': agree_form, 'disagree_form': disagree_form, 'signer': signer,
                               'is_microcontroller': is_microcontroller})

            if user.profile.user_is_microcontroller is False:
                new_singer_form = NewSignerForm()
                new_singer_form.fields['owner_name'].queryset = Profile.objects.filter(
                    user_is_microcontroller=True).values_list('user__username', flat=True)
                unsubscribe_form = NewSignerForm()
                unsubscribe_form.fields['owner_name'].queryset = Signer.objects.filter(user=request.user).values_list(
                    'owner_name__username', flat=True)
                return render(request, 'house/followers.html', {'new_singer_form': new_singer_form,
                                                                'unsubscribe_form': unsubscribe_form,
                                                                'is_microcontroller': is_microcontroller, })


# ===================== РЕГИСТРАЦИЯ, АВТОРИЗАЦИЯ, РАЗЛОГИНИВАНИЕ =====================
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'house/login.html', {"form": form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'house/register.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('MyLogin')
