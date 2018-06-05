from django.contrib import admin
from .models import *

# Register your models here.


class AdminTesis(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Tesis, AdminTesis)
admin.site.site_header = 'Portal de Administracion'