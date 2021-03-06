# Generated by Django 3.2.7 on 2022-01-11 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartoons', '0022_alter_episode_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartoon',
            name='background_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='cartoon',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='character',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='episode',
            name='screenshot',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='network',
            name='logo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='voiceactor',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
