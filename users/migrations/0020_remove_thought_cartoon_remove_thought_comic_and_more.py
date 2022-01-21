# Generated by Django 4.0 on 2021-12-27 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0019_testmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thought',
            name='cartoon',
        ),
        migrations.RemoveField(
            model_name='thought',
            name='comic',
        ),
        migrations.RemoveField(
            model_name='thought',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='thought',
            name='issue',
        ),
        migrations.AddField(
            model_name='thought',
            name='related_object',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='testmodel',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'comics'), ('model', 'comic')), models.Q(('app_label', 'comics'), ('model', 'issue')), models.Q(('app_label', 'cartoons'), ('model', 'cartoon')), models.Q(('app_label', 'cartoons'), ('model', 'episode')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='thought',
            name='thought_type',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(models.Q(('app_label', 'comics'), ('model', 'comic')), models.Q(('app_label', 'comics'), ('model', 'issue')), models.Q(('app_label', 'cartoons'), ('model', 'cartoon')), models.Q(('app_label', 'cartoons'), ('model', 'episode')), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
    ]