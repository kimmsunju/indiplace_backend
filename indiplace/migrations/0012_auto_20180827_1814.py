# Generated by Django 2.1 on 2018-08-27 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indiplace', '0011_auto_20180827_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artistinfo',
            name='memo',
            field=models.CharField(default='안녕하세요', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
