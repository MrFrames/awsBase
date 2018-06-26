# Generated by Django 2.0.6 on 2018-06-20 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0022_auto_20180617_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='pastdata',
            name='deistanceGoogle',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='pastdata',
            name='distanceAB',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='pastdata',
            name='movingTime',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='pastdata',
            name='speed',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='pastdata',
            name='totalMovingTime',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
