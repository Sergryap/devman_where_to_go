# Generated by Django 4.1.2 on 2022-10-13 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0011_auto_20221013_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='coordinate_lat',
        ),
        migrations.RemoveField(
            model_name='place',
            name='coordinate_lng',
        ),
    ]
