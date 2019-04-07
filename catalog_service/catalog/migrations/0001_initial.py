# Generated by Django 2.2 on 2019-04-07 14:52

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields.json
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_code', models.CharField(blank=True, default='', max_length=2, verbose_name='ISO Code')),
                ('name', models.CharField(max_length=40, verbose_name='Market Name')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Product Name')),
                ('product_uuid', models.UUIDField(default=uuid.uuid4, help_text='Unique identifier for product across services', unique=True, verbose_name='Unique ID for Product')),
                ('product_category', models.CharField(max_length=25)),
                ('discontinued', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated At')),
            ],
            options={
                'unique_together': {('name', 'product_category')},
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Unique ID for Event')),
                ('object_id', models.CharField(max_length=50)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('body', django_extensions.db.fields.json.JSONField(default=dict)),
                ('sent', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-time_created'],
            },
        ),
        migrations.CreateModel(
            name='CatalogEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('availability_date', models.DateField(blank=True, db_index=True, null=True, verbose_name='Product offering start')),
                ('availability_end_date', models.DateField(blank=True, db_index=True, null=True, verbose_name='Product offering ends')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated At')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalog_entries', to='catalog.Market', verbose_name='Market')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalog_entries', to='catalog.Product')),
            ],
        ),
    ]
