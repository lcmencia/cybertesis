from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

# Create your models here.


class DocumentType(models.Model):
    name = models.CharField(max_length=20)


class Person(models.Model):
    document_number = models.CharField(max_length=20)
    documen_type = models.ForeignKey('DocumentType', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Institution(models.Model):
    TYPE_CHOICES = (
        ('N', 'Nacional'),
        ('P', 'Privada'))
    name = models.CharField(max_length=50)
    description = models.TextField()
    institution_type = models.CharField(max_length=3, choices=TYPE_CHOICES)


class Faculty(models.Model):
    name = models.CharField(max_length=50)
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()
    address = models.CharField(max_length=200)


class Career(models.Model):
    name = models.CharField(max_length=50)
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
    url = models.CharField(max_length=200)
    format = models.CharField(max_length=10)
    description = models.TextField()
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)],
        help_text="Usar este formato de fecha: <YYYY>")
    tesis_type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='T')
    tutor = models.ManyToManyField(Person, related_name='tutor')
    author = models.ManyToManyField(Person, related_name='author')




