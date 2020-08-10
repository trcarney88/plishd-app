# Generated by Django 2.2.6 on 2019-11-08 04:12

import datetime
from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
        migrations.AddField(
            model_name='profile',
            name='accompInterval',
            field=models.CharField(choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly'), ('Q', 'Quarterly'), ('SA', 'Semi Annually'), ('A', 'Annually')], default='W', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='accompTaskId',
            field=models.CharField(blank=True, editable=False, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='reminderTime',
            field=models.TimeField(default=datetime.time(16, 0)),
        ),
        migrations.AddField(
            model_name='profile',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default='UTC'),
        ),
    ]