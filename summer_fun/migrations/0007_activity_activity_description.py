# Generated by Django 3.2.7 on 2021-11-22 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summer_fun', '0006_schedule_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='activity_description',
            field=models.CharField(default='fun activity', max_length=100),
            preserve_default=False,
        ),
    ]
