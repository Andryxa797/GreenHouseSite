from django.contrib import admin
from .models import DataHouse, Signer, Profile


class DataHouseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'owner', 'created_at')  # Что отображается в админке в новостях
    list_display_links = ('id', 'created_at')  # Показывает ссылку для перехода по данным полям
    search_fields = ('id', 'created_at')  # Добавления поля пойска по параметрам в скобках
    list_filter = ('id', 'created_at', 'owner')  # Позволяет фильтровать


class SignerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'owner_name', 'published', 'on_check')  # Что отображается в админке в новостях
    list_editable = ('published', 'on_check')
    list_display_links = ('id', 'user')  # Показывает ссылку для перехода по данным полям
    search_fields = (
        'user__user', 'owner_name', 'published', 'on_check')  # Добавления поля пойска по параметрам в скобках
    list_filter = ('owner_name', 'published', 'on_check')  # Позволяет фильтровать


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_is_microcontroller')  # Что отображается в админке в новостях


admin.site.register(DataHouse, DataHouseAdmin)
admin.site.register(Signer, SignerAdmin)
admin.site.register(Profile, ProfileAdmin)
