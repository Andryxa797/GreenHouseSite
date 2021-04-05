import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from house.models import Profile, Signer


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Логин'}))
    first_name = forms.CharField(label='',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    password1 = forms.CharField(label='',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'autocomplete': "off", 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserSetting(UserCreationForm):
    first_name = forms.CharField(label='Имя',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserSetting, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']


class UserContact(UserCreationForm):
    address = forms.CharField(label='Адресс',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адресс'}))
    number_telephone = forms.CharField(label='Номер телефона',
                                       widget=forms.NumberInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}))
    city = forms.CharField(label='Город',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'}))
    country = forms.CharField(label='Страна',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Страна'}))

    class Meta:
        model = User
        fields = ('address', 'number_telephone', 'city', 'country')

    def __init__(self, *args, **kwargs):
        super(UserContact, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']


class SignerDisagreeForm(forms.ModelForm):
    class Meta:
        model = Signer
        fields = ['owner_name']
        widgets = {
            'owner_name': forms.Select(attrs={"class": "form-control", "rows": 5}),
        }


class SignerAgreeForm(forms.ModelForm):
    class Meta:
        model = Signer
        fields = ['owner_name']
        widgets = {
            'owner_name': forms.Select(attrs={"class": "form-control", "rows": 5}),
        }


class OwnerAgreeForm(forms.ModelForm):
    class Meta:
        model = Signer
        fields = ['user']
        widgets = {
            'user': forms.Select(attrs={"class": "form-control", "rows": 5}),
        }

    # def __init__(self, user, *args, **kwargs):
    #     super(SignerDisagreeForm, self).__init__(*args, **kwargs)
    #     self.fields['owner_name'].queryset = Signer.objects.filter(user=user,
    #                                                                owner_name__profile__user_is_microcontroller=True).values_list(
    #         'owner_name__username', flat=True)

    # def __init__(self, *args, **kwargs):
    #     super(SignerDisagreeForm, self).__init__(*args, **kwargs)
    #     self.fields['owner_name'].queryset = Signer.objects.filter(
    #         owner_name__profile__user_is_microcontroller=True).values_list(
    #         'owner_name__username', flat=True)

    # def save(self, commit=True):
    #     self.instance.user = self.request.user
    #     return super().save(commit=commit)

    # def __str__(self):
    #     return self.owner_name

# def get_form_kwargs(self):
#     kwargs = super(NewSignerForm, self).get_form_kwargs()
#     kwargs['owner_name'] = Signer.objects.filter(user__is_staff=True)
#     return kwargs
#
#
#
# def __str__(self):
#     return self.owner_name
#
#
# def __init__(self, **kwargs):
#     super(NewSignerForm, self).__init__(**kwargs)
#     self.fields['owner_name'].queryset = Signer.objects.filter(user__is_staff=True)
#
#
# def save(self, commit=True):
#     self.instance.user = self.request.user
#     return super().save(commit=commit)
#
#
# widgets = {
#     'title': forms.TextInput(attrs={"class": "form-control", "rows": 5}),
#     'content': forms.Textarea(attrs={"class": "form-control", "rows": 5}),
#     'Category': forms.Select(attrs={"class": "form-control", "rows": 5}),
# }
#
#
# def clean_title(self):
#     title = self.cleaned_data['title']
#     if re.match(r'\d', title):
#         raise ValidationError('Название не должно начинаться с цифры')
#     return title
