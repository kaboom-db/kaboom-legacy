# Generated by Django 3.2.7 on 2021-12-24 10:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0030_auto_20211223_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='rating',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
