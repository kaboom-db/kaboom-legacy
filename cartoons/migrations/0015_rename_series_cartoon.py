# Generated by Django 4.0 on 2021-12-25 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_cartoonsubscription_rating'),
        ('cartoons', '0014_remove_character_series_series_characters'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Series',
            new_name='Cartoon',
        ),
    ]
