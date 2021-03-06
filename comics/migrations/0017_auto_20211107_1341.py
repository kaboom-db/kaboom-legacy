# Generated by Django 3.2.8 on 2021-11-07 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0016_alter_issue_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='issue_number_absolute',
            new_name='absolute_issue_number',
        ),
        migrations.AlterUniqueTogether(
            name='issue',
            unique_together={('absolute_issue_number', 'series')},
        ),
    ]
