# Generated by Django 2.1.4 on 2019-01-15 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190115_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='receive_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Receipt date'),
        ),
    ]