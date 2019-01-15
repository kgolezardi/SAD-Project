# Generated by Django 2.1.4 on 2019-01-15 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_bid_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='receive_date',
            field=models.DateTimeField(null=True, verbose_name='Receipt date'),
        ),
        migrations.AddField(
            model_name='auction',
            name='received',
            field=models.BooleanField(default=False),
        ),
    ]