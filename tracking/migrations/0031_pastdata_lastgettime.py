# Generated by Django 2.0.6 on 2018-06-29 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0030_auto_20180628_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='pastdata',
            name='lastGetTime',
            field=models.DateTimeField(default='2018-06-28T12:00:00-0000'),
        ),
    ]