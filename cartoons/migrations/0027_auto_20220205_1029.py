# Generated by Django 3.2.7 on 2022-02-05 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartoons', '0026_character_alias'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='voice_actor',
        ),
        migrations.AddField(
            model_name='character',
            name='voice_actors',
            field=models.ManyToManyField(blank=True, to='cartoons.VoiceActor'),
        ),
    ]