# Generated by Django 2.0.6 on 2018-06-03 14:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesis', '0009_tesis_added_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tesis',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 3, 10, 13, 23, 28924)),
        ),
    ]