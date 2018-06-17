from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.

admin.site.site_header = 'Portal de Administracion'


class AdminTesis(admin.ModelAdmin):
    list_display = ('id', 'title')


class AdminInstitution(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Tesis, AdminTesis)
admin.site.register(Institution, AdminInstitution)


class ProfileInline(admin.StackedInline):
    model = DataEntry
    can_delete = False
    verbose_name_plural = 'DataEntry'
    fk_name = 'user'


class CustomUserDataEntryAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_institution')
    list_select_related = ('dataentry',)

    def get_institution(self, instance):
        return instance.dataentry.institution

    get_institution.short_description = 'Universidad'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserDataEntryAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserDataEntryAdmin)
