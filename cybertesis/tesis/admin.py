from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.

admin.site.site_header = 'Portal de Administración'


class AdminTesis(admin.ModelAdmin):
    list_display = ('id', 'title')


class AdminInstitution(admin.ModelAdmin):
    list_display = ('id', 'name')


class AdminCategory(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'category_fa_icon')


class AdminSubCategory(admin.ModelAdmin):
    list_display = ('id', 'sub_category_name', 'sub_category_fa_icon', 'get_category')

    def get_category(self, instance):
        cats = ''
        categories_list = instance.categories.all()
        for cat in categories_list:
            cats += '' + cat.category_name + ', '
        if cats[-2:] == ', ':
            cats = cats[:-2]

        return cats

    get_category.short_description = 'Categorías'


class AdminCareer(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_faculty', 'get_institution')

    def get_faculty(self, instance):
        return instance.faculty

    get_faculty.short_description = 'Facultad'

    def get_institution(self, instance):
        return instance.faculty.institution

    get_institution.short_description = 'Universidad'


class AdminFaculty(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_institution')

    def get_institution(self, instance):
        return instance.institution

    get_institution.short_description = 'Universidad'


# admin.site.register(Tesis, AdminTesis)
admin.site.register(Institution, AdminInstitution)
admin.site.register(Category, AdminCategory)
admin.site.register(SubCategory, AdminSubCategory)
admin.site.register(Career, AdminCareer)
admin.site.register(Faculty, AdminFaculty)


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
