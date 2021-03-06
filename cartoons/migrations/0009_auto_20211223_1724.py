# Generated by Django 3.2.7 on 2021-12-23 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cartoons', '0008_character_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='genre',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='network',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cartoons.network'),
        ),
    ]
