# Generated by Django 2.0.6 on 2018-06-06 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0014_auto_20180606_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='place2',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracking.section'),
        ),
        migrations.AlterField(
            model_name='place2',
            name='name',
            field=models.CharField(default='some_name', max_length=200),
            preserve_default=False,
        ),
    ]
