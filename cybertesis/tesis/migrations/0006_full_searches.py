# Generated by Django 2.0.6 on 2018-06-03 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesis', '0005_auto_20180602_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Full',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('year', models.TextField()),
                ('career_id', models.TextField()),
                ('career_name', models.TextField()),
                ('faculty_name', models.TextField()),
                ('place', models.TextField()),
                ('institution_id', models.TextField()),
                ('institution_name', models.TextField()),
                ('authors', models.TextField()),
                ('tutors', models.TextField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Searches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField()),
            ],
        ),
    ]
