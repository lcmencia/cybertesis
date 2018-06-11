# Generated by Django 2.0.6 on 2018-06-11 10:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tesis.models


class Migration(migrations.Migration):

    dependencies = [
        ('tesis', '0012_auto_20180603_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='PyDepartments',
            fields=[
                ('department_id', models.IntegerField(db_column='department_id', primary_key=True, serialize=False)),
                ('department_name', models.CharField(db_column='department_name', max_length=100)),
                ('department_capital', models.CharField(db_column='department_capital', max_length=100)),
                ('lon', models.FloatField(db_column='lon', null=True)),
            ],
            options={
                'db_table': 'tesis_py_departments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(db_column='category_name', max_length=100, unique=True)),
                ('category_fa_icon', models.CharField(db_column='category_fa_icon', max_length=100, null=True)),
            ],
            options={
                'db_table': 'tesis_category',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category_name', models.CharField(db_column='sub_category_name', max_length=100, unique=True)),
                ('sub_category_fa_icon', models.CharField(db_column='sub_category_fa_icon', max_length=100, null=True)),
                ('categories', models.ManyToManyField(db_column='categories', to='tesis.Category')),
            ],
            options={
                'db_table': 'tesis_sub_category',
            },
        ),
        migrations.CreateModel(
            name='TesisRanking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_vote', models.DateTimeField(auto_now=True, db_column='date_vote')),
                ('value', models.IntegerField(default=0)),
                ('vote_by', models.IntegerField(null=True)),
                ('user_name', models.TextField()),
                ('user_email', models.TextField(unique=True)),
            ],
            options={
                'db_table': 'tesis_tesis_ranking',
            },
        ),
        migrations.AlterModelOptions(
            name='tesis',
            options={'verbose_name_plural': 'Tesis'},
        ),
        migrations.AddField(
            model_name='institution',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=tesis.models.Institution.get_upload_file_name),
        ),
        migrations.AlterField(
            model_name='tesis',
            name='added_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='tesisranking',
            name='tesis_id',
            field=models.ForeignKey(db_column='tesis_id', on_delete=django.db.models.deletion.CASCADE, to='tesis.Tesis'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='department_id',
            field=models.ForeignKey(db_column='department_id', default=0, on_delete=django.db.models.deletion.CASCADE, to='tesis.PyDepartments'),
        ),
        migrations.AddField(
            model_name='tesis',
            name='sub_category',
            field=models.ManyToManyField(db_column='sub_category', to='tesis.SubCategory'),
        ),
    ]
