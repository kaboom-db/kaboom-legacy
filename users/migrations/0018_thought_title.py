# Generated by Django 4.0 on 2021-12-25 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_cartoonsubscription_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='thought',
            name='title',
            field=models.CharField(default='title', max_length=250),
            preserve_default=False,
        ),
    ]
