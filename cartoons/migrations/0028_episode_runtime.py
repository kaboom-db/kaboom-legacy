# Generated by Django 3.2.7 on 2022-02-07 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartoons', '0027_auto_20220205_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='runtime',
            field=models.PositiveIntegerField(default=10),
            preserve_default=False,
        ),
    ]