# Generated by Django 3.2.7 on 2022-02-01 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartoons', '0025_auto_20220112_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='alias',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
