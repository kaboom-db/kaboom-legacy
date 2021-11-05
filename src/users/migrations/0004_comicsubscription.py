# Generated by Django 3.2.8 on 2021-11-05 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comics', '0013_alter_issue_issue_number'),
        ('users', '0003_delete_userbio'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComicSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comics.series')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
