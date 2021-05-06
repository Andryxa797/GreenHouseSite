from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    user_is_microcontroller = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='media/%Y/%m/%d', default='meeting.jpg')
    address = models.CharField(blank=True, max_length=250)
    number_telephone = models.CharField(blank=True, max_length=15)
    city = models.CharField(blank=True, max_length=250)
    country = models.CharField(blank=True, max_length=250)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class DataHouse(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата записи', auto_now_add=True)
    temp_greenhouse_upstairs = models.DecimalField(max_digits=20, decimal_places=6, verbose_name='Температура в теплице, в верхней части')
    temp_greenhouse_downstairs = models.DecimalField(max_digits=20, decimal_places=6, verbose_name='Температура в теплице, в нижней части')
    temp_greenhouse_in_ground = models.DecimalField(max_digits=20, decimal_places=6, verbose_name='Температура в теплице, в земле')
    temp_street = models.DecimalField(max_digits=20, decimal_places=6, verbose_name='Температура на улице')
    humidity_greenhouse = models.DecimalField(max_digits=20, decimal_places=6, verbose_name='Влажность в теплице')
    humidity_greenhouse_in_ground = models.IntegerField(verbose_name='Влажность в теплице, в земли')
    servo_turn_upstairs = models.IntegerField(verbose_name='Поворот нижнего сервопривода')
    servo_turn_downstairs = models.IntegerField(verbose_name='Поворот верхнего сервопривода')
    conditions_load_one = models.BooleanField(verbose_name='Первая нагрузка')
    conditions_load_two = models.BooleanField(verbose_name='Вторая нагрузка')
    conditions_load_three = models.BooleanField(verbose_name='Третья нагрузка')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
                              verbose_name='Владелец записи',
                              related_name='my_data')

    class Meta:
        verbose_name = 'Данные'  # Для изменения названия, раньше приложение называлась, как DataHouse, теперь Данные
        verbose_name_plural = 'Данные'  # Название во множественном числе
        ordering = ['-created_at']  # Здесь мы говорим как будем сортировать наши новости, а именно сначала
        # новые, но если будут по этому критерию  совпадения то по умолчанию будет использоваться следующий критерий


class Signer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Подписчик',
                             related_name='user')
    owner_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Админ группы',
                                   related_name='owner_name', blank=True)
    published = models.BooleanField(default=False, verbose_name='Опубликованно ли?')
    on_check = models.BooleanField(default=False, verbose_name='Проверянно ли?')

    class Meta:
        verbose_name = 'Система подписок'
        verbose_name_plural = 'Система подписок'  # Название во множественном числе
        unique_together = ('user', 'owner_name')  # Множество полей, комбинация значений которых должна быть уникальна
