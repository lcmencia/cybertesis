# Generated by Django 2.0.6 on 2018-06-03 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesis', '0007_auto_20180603_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searches',
            name='count',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
