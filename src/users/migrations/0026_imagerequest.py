# Generated by Django 3.2.7 on 2022-01-12 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0025_delete_thoughttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('object_type', models.CharField(choices=[('COMIC_PUBLISHER', 'comic_publisher'), ('COMIC_STAFF', 'comic_staff'), ('COMIC_CHARACTER', 'comic_character'), ('COMIC_SERIES', 'comic_series'), ('COMIC_ISSUE', 'comic_issue'), ('CARTOON_VOICEACTOR', 'cartoon_voiceactor'), ('CARTOON_NETWORK', 'cartoon_network'), ('CARTOON_CHARACTER', 'cartoon_character'), ('CARTOON_SERIES', 'cartoon_series'), ('CARTOON_EPISODE', 'cartoon_episode')], max_length=50)),
                ('request_field', models.CharField(choices=[('COVER', 'Cover'), ('BACKGROUND', 'Background'), ('GENERIC', 'Generic'), ('LOGO', 'Logo')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]