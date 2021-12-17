# Generated by Django 3.2.8 on 2021-11-07 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0013_alter_issue_issue_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='alias',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='characters',
            field=models.ManyToManyField(null=True, to='comics.Character'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='staff',
            field=models.ManyToManyField(null=True, to='comics.Staff'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='website',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='image',
            field=models.URLField(null=True),
        ),
    ]