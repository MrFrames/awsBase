# Generated by Django 2.0.6 on 2018-06-02 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_auto_20180602_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unnamed', max_length=200)),
                ('nameStart', models.CharField(default='London', max_length=200)),
                ('nameEnd', models.CharField(default='Dover', max_length=200)),
                ('latStart', models.FloatField(default=51.5285582)),
                ('lonStart', models.FloatField(default=-0.2416789)),
                ('latEnd', models.FloatField(default=51.1262831)),
                ('lonEnd', models.FloatField(default=1.2834798)),
            ],
        ),
        migrations.AlterField(
            model_name='pastdata',
            name='time',
            field=models.DateTimeField(default='2018-04-15 14:30:59'),
        ),
    ]
