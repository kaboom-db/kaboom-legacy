# Generated by Django 3.2.8 on 2021-11-10 18:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20211110_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readissue',
            name='watched_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]