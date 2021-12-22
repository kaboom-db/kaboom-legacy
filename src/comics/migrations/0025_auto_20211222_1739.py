# Generated by Django 3.2.7 on 2021-12-22 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0024_auto_20211222_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='series',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='comics.statusoptions'),
        ),
    ]
