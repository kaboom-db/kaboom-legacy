# Generated by Django 3.2.7 on 2021-12-25 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0031_series_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='age',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]