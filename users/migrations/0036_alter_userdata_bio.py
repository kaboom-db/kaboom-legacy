# Generated by Django 3.2.7 on 2022-02-23 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0035_alter_userdata_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
