# Generated by Django 2.1 on 2018-08-30 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indiplace', '0014_auto_20180830_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artistinfo',
            name='faceBook',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='artistinfo',
            name='instagram',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='artistinfo',
            name='memo',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='artistinfo',
            name='youtube',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='faceBookId',
            field=models.CharField(blank=True, default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='kakaoTalkId',
            field=models.CharField(blank=True, default='', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='performance',
            name='place',
            field=models.CharField(blank=True, default='', max_length=20),
            preserve_default=False,
        ),
    ]