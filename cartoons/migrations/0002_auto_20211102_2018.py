# Generated by Django 3.2.8 on 2021-11-02 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartoons', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cartoon',
            new_name='Series',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='cartoon',
            new_name='series',
        ),
    ]
