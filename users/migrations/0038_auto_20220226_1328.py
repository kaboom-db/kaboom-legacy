# Generated by Django 3.2.7 on 2022-02-26 13:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0037_auto_20220224_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartoonsubscription',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='comicsubscription',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
