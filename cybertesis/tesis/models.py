from time import time

import django
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


# Create your models here.


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
    name = models.TextField()
    description = models.TextField(null=True)
    institution_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    logo = models.ImageField(null=True, blank=True, upload_to=get_upload_file_name)


class PyDepartments(models.Model):
    department_id = models.IntegerField(primary_key=True, db_column='department_id')
    department_name = models.CharField(max_length=100, null=False, blank=False, db_column='department_name')
    department_capital = models.CharField(max_length=100, null=False, blank=False, db_column='department_capital')
    lat = models.FloatField(null=True, db_column='lat'),
    lon = models.FloatField(null=True, db_column='lon')

    class Meta:
        db_table = 'tesis_py_departments'
        managed = False


class Faculty(models.Model):
    name = models.TextField(null=True)
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)
    address = models.CharField(max_length=200, null=True)
    department_id = models.ForeignKey('PyDepartments', on_delete=models.CASCADE, to_field='department_id', default=0, db_column='department_id')


class Career(models.Model):
    name = models.TextField()
    postgraduate = models.BooleanField()
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE)


class Tesis(models.Model):
    TYPE_CHOICES = (
        ('T', 'Tesis'),
        ('TD', 'Tesis Doctoral'),
        ('MS', 'Maestría'),
        ('TM', 'Tesis Maestría')
    )
    title = models.CharField(max_length=200)
    career = models.ForeignKey('Career', on_delete=models.CASCADE)
    url = models.CharField(max_length=200, null=True)
    format = models.CharField(max_length=10, null=True)
    description = models.TextField(null=True)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)],
        help_text="Usar este formato de fecha: <YYYY>")
    tesis_type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='T')
    tutor = models.ManyToManyField(Person, related_name='tutor')
    author = models.ManyToManyField(Person, related_name='author')
    added_date = models.DateTimeField(default=django.utils.timezone.now)
    sub_category = models.ManyToManyField('SubCategory', db_column='sub_category')

    class Meta:
        verbose_name_plural = 'Tesis'


class Full(models.Model):
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

    class Meta:
        managed = False


class Searches(models.Model):
    word = models.TextField()
    count = models.PositiveIntegerField(null=True)


class TesisRanking(models.Model):
    tesis_id = models.ForeignKey('Tesis', on_delete=models.CASCADE, db_column='tesis_id')
    date_vote = models.DateTimeField(auto_now=True, db_column='date_vote')
    vote_by = models.IntegerField(null=True)

    class Meta:
        db_table = 'tesis_tesis_ranking'


class Category(models.Model):
    category_name = models.CharField(max_length=100, db_column='category_name', unique=True)
    category_fa_icon = models.CharField(max_length=100, db_column='category_fa_icon', null=True)

    class Meta:
        db_table = 'tesis_category'


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=100, db_column='sub_category_name', unique=True)
    sub_category_fa_icon = models.CharField(max_length=100, db_column='sub_category_fa_icon', null=True)
    categories = models.ManyToManyField('Category', db_column='categories')

    class Meta:
        db_table = 'tesis_sub_category'
