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


class Institution(models.Model):
    TYPE_CHOICES = (
        ('N', 'Nacional'),
        ('P', 'Privada'))
    name = models.TextField()
    description = models.TextField(null=True)
    institution_type = models.CharField(max_length=3, choices=TYPE_CHOICES)


class Faculty(models.Model):
    name = models.TextField(null=True)
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)
    address = models.CharField(max_length=200, null=True)


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
    added_date = models.DateTimeField(default=datetime.now())


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

    class Meta:
        managed = False


class Searches(models.Model):
    word = models.TextField()
    count = models.PositiveIntegerField(null=True)
