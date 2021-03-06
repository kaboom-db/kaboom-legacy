# Generated by Django 3.2.7 on 2022-01-11 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0037_alter_issue_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='comic',
            name='background_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='comic',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='issue',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='logo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='staff',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
