# Generated by Django 2.2 on 2019-04-09 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='catalogentry',
            unique_together={('market', 'product')},
        ),
    ]