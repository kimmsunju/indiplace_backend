# Generated by Django 2.1 on 2018-08-23 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indiplace', '0007_auto_20180823_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artistinfo',
            name='memberId',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='artist_info', to='indiplace.Member'),
        ),
    ]
