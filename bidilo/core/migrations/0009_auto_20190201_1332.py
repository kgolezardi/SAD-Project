# Generated by Django 2.1.4 on 2019-02-01 10:02

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190201_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='picture',
            field=models.ImageField(default='auction_images/7e6b2e82512d4c28b0ab4aef7195bc06.jpg', help_text='The main image for the auction', upload_to=core.models.get_image_filename, validators=[core.models.auction_picture_validator]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auction',
            name='description',
            field=models.TextField(help_text='Enter a more detailed description of the item', max_length=1000),
        ),
        migrations.AlterField(
            model_name='auction',
            name='short_description',
            field=models.TextField(help_text='Enter a brief description of the item to showin the auctions list', max_length=500),
        ),
    ]
