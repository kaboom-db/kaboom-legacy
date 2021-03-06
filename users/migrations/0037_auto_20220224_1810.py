# Generated by Django 3.2.7 on 2022-02-24 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_alter_userdata_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thought',
            name='thought_type',
        ),
        migrations.RemoveField(
            model_name='thought',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='userlikedthought',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='userlikedthought',
            name='thought',
        ),
        migrations.RemoveField(
            model_name='userlikedthought',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Thought',
        ),
        migrations.DeleteModel(
            name='UserLikedThought',
        ),
    ]
