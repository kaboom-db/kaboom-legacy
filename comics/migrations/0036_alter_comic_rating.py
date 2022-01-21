# Generated by Django 4.0 on 2021-12-25 17:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0035_alter_comic_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='rating',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]