# Generated by Django 2.1.4 on 2019-01-04 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='credit',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
