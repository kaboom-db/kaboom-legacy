# Generated by Django 3.2.7 on 2021-12-25 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0032_staff_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
