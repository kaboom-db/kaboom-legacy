# Generated by Django 3.2.8 on 2021-11-10 18:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20211110_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='readissue',
            name='watched_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 10, 18, 49, 1, 623839, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='readissue',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='readissue',
            name='rating',
        ),
    ]
