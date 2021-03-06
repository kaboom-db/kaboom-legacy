# Generated by Django 3.2.8 on 2021-10-30 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0010_auto_20211030_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='issue_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='issue',
            name='issue_number',
            field=models.IntegerField(default=1, unique=True),
        ),
    ]
