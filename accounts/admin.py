from django.contrib import admin
from .models import UserProfileInfo
from e_store.models import Order


class UserProfileInfoAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'get_first_last_names')
    search_fields = ('get_id', 'get_first_last_names')

    def get_id(self, obj):
        return obj.user.id

    def get_first_last_names(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    get_id.short_description = 'id'
    get_first_last_names.short_description = 'Имя и Фамилия'


admin.site.register(UserProfileInfo, UserProfileInfoAdmin)