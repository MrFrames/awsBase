# Generated by Django 2.0.6 on 2018-06-15 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0019_section_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetup',
            name='show',
            field=models.CharField(choices=[('True', 'Show'), ('False', 'Hide')], default='True', max_length=20),
        ),
    ]
