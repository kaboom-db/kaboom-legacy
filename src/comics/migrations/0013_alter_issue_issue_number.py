# Generated by Django 3.2.8 on 2021-10-30 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0012_auto_20211030_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue_number',
            field=models.CharField(max_length=10),
        ),
    ]
