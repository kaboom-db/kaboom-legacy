# Generated by Django 3.2.7 on 2022-02-15 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cartoons', '0035_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='base_of_operations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cartoons.location'),
        ),
    ]
