# Generated by Django 2.0.6 on 2018-06-02 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_meetup'),
    ]

    operations = [
        migrations.CreateModel(
            name='place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='nowhere', max_length=200)),
                ('lat', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField(max_length=10000)),
                ('place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='postPlace', to='tracking.place')),
            ],
        ),
        migrations.RemoveField(
            model_name='meetup',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='meetup',
            name='lon',
        ),
        migrations.RemoveField(
            model_name='section',
            name='latEnd',
        ),
        migrations.RemoveField(
            model_name='section',
            name='latStart',
        ),
        migrations.RemoveField(
            model_name='section',
            name='lonEnd',
        ),
        migrations.RemoveField(
            model_name='section',
            name='lonStart',
        ),
        migrations.RemoveField(
            model_name='section',
            name='nameEnd',
        ),
        migrations.RemoveField(
            model_name='section',
            name='nameStart',
        ),
        migrations.AlterField(
            model_name='meetup',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meetUpSection', to='tracking.section'),
        ),
        migrations.AddField(
            model_name='post',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='postSection', to='tracking.section'),
        ),
        migrations.AddField(
            model_name='meetup',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meetUpPlace', to='tracking.place'),
        ),
        migrations.AddField(
            model_name='section',
            name='endPlace',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sectionEnd', to='tracking.place'),
        ),
        migrations.AddField(
            model_name='section',
            name='startPlace',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sectionStart', to='tracking.place'),
        ),
    ]
