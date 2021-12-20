# Generated by Django 3.2.7 on 2021-12-20 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0019_auto_20211220_0914'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cartoons', '0003_character_series'),
        ('users', '0014_rename_watchedcartoon_watchedepisode'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThoughtType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Thought',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_content', models.TextField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('num_of_likes', models.IntegerField(default=0)),
                ('cartoon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cartoons.series')),
                ('comic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='comics.series')),
                ('episode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cartoons.episode')),
                ('issue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='comics.issue')),
                ('thought_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.thoughttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('thought', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.thought')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
