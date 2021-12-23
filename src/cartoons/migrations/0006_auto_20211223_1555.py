# Generated by Django 3.2.7 on 2021-12-23 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartoons', '0005_series_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='voiceactor',
            name='biography',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='voiceactor',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='voiceactor',
            name='date_of_death',
            field=models.DateField(blank=True, null=True),
        ),
    ]
