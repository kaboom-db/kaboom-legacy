# Generated by Django 3.2.8 on 2021-10-28 18:58

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0006_auto_20211028_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='release_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='series',
            name='status',
            field=models.CharField(choices=[('COMPLETED', 'Completed'), ('RELEASING', 'Releasing'), ('PLANNED', 'Planned')], default='Completed', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='series',
            name='year_started',
            field=models.IntegerField(default=2021, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
            preserve_default=False,
        ),
    ]
