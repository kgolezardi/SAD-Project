# Generated by Django 2.1.4 on 2019-02-06 02:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20190205_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
