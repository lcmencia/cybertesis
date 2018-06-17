from time import time

import django
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class DocumentType(models.Model):
    name = models.CharField(max_length=20)


class Person(models.Model):
    document_number = models.CharField(max_length=20, null=True)
    document_type = models.ForeignKey('DocumentType', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Institution(models.Model):

    def get_upload_file_name(instance, filename):
        return "institution_logo/%s_%s" % (str(time()).replace('.', '_'), filename)

    TYPE_CHOICES = (
        ('N', 'Nacional'),
        ('P', 'Privada'))
    name = models.TextField(verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción', null=True, blank=True)
    institution_type = models.CharField(verbose_name='Tipo', max_length=3, choices=TYPE_CHOICES)
    logo = models.ImageField(verbose_name='Logo', null=True, blank=True, upload_to=get_upload_file_name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Universidad'
        verbose_name_plural = 'Universidades'


class PyDepartments(models.Model):
    department_id = models.AutoField(primary_key=True, db_column='department_id')
    department_name = models.CharField(max_length=100, null=False, blank=False, db_column='department_name')
    department_capital = models.CharField(max_length=100, null=False, blank=False, db_column='department_capital')
    lat = models.FloatField(null=True, db_column='lat')
    lon = models.FloatField(null=True, db_column='lon')

    class Meta:
        db_table = 'tesis_py_departments'

    def __str__(self):
        return self.department_name


class Faculty(models.Model):
    name = models.TextField(verbose_name='Nombre', null=True)
    place = models.TextField(verbose_name='Lugar', max_length=100, null=True, blank=True)
    lon = models.FloatField(verbose_name='Latitud', null=True, blank=True)
    lat = models.FloatField(verbose_name='Longitud', null=True, blank=True)
    address = models.TextField(verbose_name='Dirección', null=True, blank=True)
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, verbose_name='Universidad')
    department_id = models.ForeignKey('PyDepartments', on_delete=models.CASCADE, to_field='department_id', default=18,
                                      db_column='department_id', verbose_name='Departamento')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Facultad'
        verbose_name_plural = 'Facultades'


class Career(models.Model):
    name = models.TextField(verbose_name='Nombre')
    postgraduate = models.BooleanField(verbose_name='¿Es postgrado?')
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, verbose_name='Facultad')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'


class Tesis(models.Model):
    TYPE_CHOICES = (
        ('T', 'Tesis'),
        ('TD', 'Tesis Doctoral'),
        ('MS', 'Maestría'),
        ('TM', 'Tesis Maestría')
    )
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    career = models.ForeignKey('Career', on_delete=models.CASCADE)
    url = models.TextField(null=True, blank=True)
    format = models.TextField(null=True, blank=True)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)],
        help_text="Usar este formato de fecha: <YYYY>")
    tesis_type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='T')
    added_date = models.DateTimeField(default=django.utils.timezone.now)
    sub_category = models.ManyToManyField('SubCategory', db_column='sub_category')
    tutor = models.ManyToManyField(Person, related_name='tutor')
    author = models.ManyToManyField(Person, related_name='author')

    class Meta:
        verbose_name_plural = 'Tesis'

    def __str__(self):
        return self.title


class Full(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    description = models.TextField()
    year = models.PositiveIntegerField()
    career_id = models.TextField()
    career_name = models.TextField()
    faculty_name = models.TextField()
    place = models.TextField()
    institution_id = models.TextField()
    institution_name = models.TextField()
    authors = models.TextField()
    tutors = models.TextField()
    added_date = models.DateTimeField()
    rating = models.IntegerField()
    cats_id = models.TextField()
    cats_name = models.TextField()
    subs_id = models.TextField()
    subs_name = models.TextField()

    class Meta:
        managed = False


class Searches(models.Model):
    word = models.TextField()
    count = models.PositiveIntegerField(null=True)


class TesisRanking(models.Model):
    tesis_id = models.ForeignKey('Tesis', on_delete=models.CASCADE, db_column='tesis_id')
    date_vote = models.DateTimeField(auto_now=True, db_column='date_vote')
    value = models.IntegerField(default=0)
    vote_by = models.IntegerField(null=True)
    user_name = models.TextField()
    user_email = models.TextField()

    class Meta:
        db_table = 'tesis_tesis_ranking'
        unique_together = ('tesis_id', 'user_email')


class Category(models.Model):
    category_name = models.CharField(verbose_name='Nombre', max_length=100, db_column='category_name', unique=True)
    category_fa_icon = models.CharField(verbose_name='Icono Material o FA', max_length=100,
                                        default='<i class="material-icons">bubble_chart</i>',
                                        db_column='category_fa_icon', null=True)

    class Meta:
        db_table = 'tesis_category'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    sub_category_name = models.CharField(verbose_name='Nombre', max_length=100, db_column='sub_category_name',
                                         unique=True)
    sub_category_fa_icon = models.CharField(verbose_name='Icono Material o FA', max_length=100,
                                            default='<i class="material-icons">bubble_chart</i>',
                                            db_column='sub_category_fa_icon', null=True, blank=True)
    categories = models.ManyToManyField('Category', db_column='categories')

    class Meta:
        db_table = 'tesis_sub_category'
        verbose_name = 'Sub Categoría'
        verbose_name_plural = 'Sub Categorías'

    def __str__(self):
        return self.sub_category_name


class DataEntry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        DataEntry.objects.create(user=instance)
    instance.dataentry.save()
