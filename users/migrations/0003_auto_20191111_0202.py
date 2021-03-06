# Generated by Django 2.2.6 on 2019-11-11 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20191108_0412'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='notificationType',
            field=models.CharField(choices=[('E', 'Email')], default='E', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='accompInterval',
            field=models.CharField(choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly'), ('Q', 'Quarterly'), ('SA', 'Semi Annually'), ('A', 'Annually')], default='W', max_length=2),
        ),
    ]
