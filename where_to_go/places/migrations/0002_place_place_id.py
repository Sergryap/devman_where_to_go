# Generated by Django 3.2.16 on 2022-10-06 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='place_id',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
