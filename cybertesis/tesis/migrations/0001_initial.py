# Generated by Django 2.0.6 on 2018-06-16 22:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tesis.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Full',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('year', models.PositiveIntegerField()),
                ('career_id', models.TextField()),
                ('career_name', models.TextField()),
                ('faculty_name', models.TextField()),
                ('place', models.TextField()),
                ('institution_id', models.TextField()),
                ('institution_name', models.TextField()),
                ('authors', models.TextField()),
                ('tutors', models.TextField()),
                ('added_date', models.DateTimeField()),
                ('rating', models.IntegerField()),
                ('cats_id', models.TextField()),
                ('cats_name', models.TextField()),
                ('subs_id', models.TextField()),
                ('subs_name', models.TextField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Nombre')),
                ('postgraduate', models.BooleanField(verbose_name='¿Es postgrado?')),
            ],
            options={
                'verbose_name': 'Carrera',
                'verbose_name_plural': 'Carreras',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(db_column='category_name', max_length=100, unique=True, verbose_name='Nombre')),
                ('category_fa_icon', models.CharField(db_column='category_fa_icon', default='<i class="material-icons">bubble_chart</i>', max_length=100, null=True, verbose_name='Icono Material o FA')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'db_table': 'tesis_category',
            },
        ),
        migrations.CreateModel(
            name='DataEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(null=True, verbose_name='Nombre')),
                ('place', models.TextField(blank=True, max_length=100, null=True, verbose_name='Lugar')),
                ('lon', models.FloatField(blank=True, null=True, verbose_name='Latitud')),
                ('lat', models.FloatField(blank=True, null=True, verbose_name='Longitud')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Dirección')),
            ],
            options={
                'verbose_name': 'Facultad',
                'verbose_name_plural': 'Facultades',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Nombre')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('institution_type', models.CharField(choices=[('N', 'Nacional'), ('P', 'Privada')], max_length=3, verbose_name='Tipo')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=tesis.models.Institution.get_upload_file_name, verbose_name='Logo')),
            ],
            options={
                'verbose_name': 'Universidad',
                'verbose_name_plural': 'Universidades',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_number', models.CharField(max_length=20, null=True)),
                ('name', models.CharField(max_length=100)),
                ('document_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tesis.DocumentType')),
            ],
        ),
        migrations.CreateModel(
            name='PyDepartments',
            fields=[
                ('department_id', models.AutoField(db_column='department_id', primary_key=True, serialize=False)),
                ('department_name', models.CharField(db_column='department_name', max_length=100)),
                ('department_capital', models.CharField(db_column='department_capital', max_length=100)),
                ('lat', models.FloatField(db_column='lat', null=True)),
                ('lon', models.FloatField(db_column='lon', null=True)),
            ],
            options={
                'db_table': 'tesis_py_departments',
            },
        ),
        migrations.CreateModel(
            name='Searches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
                ('count', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category_name', models.CharField(db_column='sub_category_name', max_length=100, unique=True, verbose_name='Nombre')),
                ('sub_category_fa_icon', models.CharField(blank=True, db_column='sub_category_fa_icon', default='<i class="material-icons">bubble_chart</i>', max_length=100, null=True, verbose_name='Icono Material o FA')),
                ('categories', models.ManyToManyField(db_column='categories', to='tesis.Category')),
            ],
            options={
                'verbose_name': 'Sub Categoría',
                'verbose_name_plural': 'Sub Categorías',
                'db_table': 'tesis_sub_category',
            },
        ),
        migrations.CreateModel(
            name='Tesis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('format', models.TextField(blank=True, null=True)),
                ('year', models.PositiveIntegerField(help_text='Usar este formato de fecha: <YYYY>', validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2018)])),
                ('tesis_type', models.CharField(choices=[('T', 'Tesis'), ('TD', 'Tesis Doctoral'), ('MS', 'Maestría'), ('TM', 'Tesis Maestría')], default='T', max_length=3)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ManyToManyField(related_name='author', to='tesis.Person')),
                ('career', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tesis.Career')),
                ('sub_category', models.ManyToManyField(db_column='sub_category', to='tesis.SubCategory')),
                ('tutor', models.ManyToManyField(related_name='tutor', to='tesis.Person')),
            ],
            options={
                'verbose_name_plural': 'Tesis',
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
                ('user_email', models.TextField()),
                ('tesis_id', models.ForeignKey(db_column='tesis_id', on_delete=django.db.models.deletion.CASCADE, to='tesis.Tesis')),
            ],
            options={
                'db_table': 'tesis_tesis_ranking',
            },
        ),
        migrations.AddField(
            model_name='faculty',
            name='department_id',
            field=models.ForeignKey(db_column='department_id', default=18, on_delete=django.db.models.deletion.CASCADE, to='tesis.PyDepartments', verbose_name='Departamento'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tesis.Institution', verbose_name='Universidad'),
        ),
        migrations.AddField(
            model_name='dataentry',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tesis.Institution'),
        ),
        migrations.AddField(
            model_name='dataentry',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='career',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tesis.Faculty', verbose_name='Facultad'),
        ),
        migrations.AlterUniqueTogether(
            name='tesisranking',
            unique_together={('tesis_id', 'user_email')},
        ),
    ]
