# Generated by Django 3.2.8 on 2021-11-07 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0014_auto_20211107_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='alias',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='characters',
            field=models.ManyToManyField(blank=True, to='comics.Character'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='staff',
            field=models.ManyToManyField(blank=True, to='comics.Staff'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
