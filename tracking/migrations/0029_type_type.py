# Generated by Django 2.0.6 on 2018-06-27 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0028_auto_20180627_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='type',
            field=models.CharField(choices=[('poly', 'poly'), ('BICYCLING', 'cycling'), ('DRIVING', 'walking')], default='BICYCLING', max_length=100),
            preserve_default=False,
        ),
    ]