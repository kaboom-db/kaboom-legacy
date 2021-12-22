# Generated by Django 3.2.7 on 2021-12-22 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartoons', '0004_auto_20211222_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='status',
            field=models.CharField(choices=[('COMPLETED', 'Completed'), ('RELEASING', 'Releasing'), ('PLANNED', 'Planned')], default='ffe', max_length=50),
            preserve_default=False,
        ),
    ]
