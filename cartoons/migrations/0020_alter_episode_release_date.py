# Generated by Django 3.2.8 on 2022-01-01 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartoons', '0019_auto_20220101_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='release_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
