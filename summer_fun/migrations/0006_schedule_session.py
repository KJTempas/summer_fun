# Generated by Django 3.2.7 on 2021-10-22 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summer_fun', '0005_auto_20210923_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='session',
            field=models.CharField(choices=[('1', 'one'), ('2', 'two'), ('3', 'three')], default=1, max_length=1),
            preserve_default=False,
        ),
    ]