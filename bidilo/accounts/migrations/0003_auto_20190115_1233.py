# Generated by Django 2.1.4 on 2019-01-15 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(default='Here', help_text='Address for other users to send you the items you buy.', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='John Nash', max_length=50, verbose_name='Display Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='09123456789', max_length=12),
            preserve_default=False,
        ),
    ]
