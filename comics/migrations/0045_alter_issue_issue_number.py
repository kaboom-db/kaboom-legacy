# Generated by Django 3.2.7 on 2022-02-17 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0044_alter_comic_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue_number',
            field=models.CharField(max_length=50),
        ),
    ]