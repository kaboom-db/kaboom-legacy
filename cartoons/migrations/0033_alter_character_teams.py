# Generated by Django 3.2.7 on 2022-02-12 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartoons', '0032_auto_20220212_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='teams',
            field=models.ManyToManyField(blank=True, to='cartoons.Team'),
        ),
    ]
