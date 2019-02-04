# Generated by Django 2.1.4 on 2019-02-04 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auctionimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='state',
            field=models.CharField(choices=[(0, 'pending'), (1, 'approved'), (2, 'rejected')], default=0, max_length=10),
        ),
    ]
