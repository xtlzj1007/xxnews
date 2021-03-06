# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-03 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '评论内容', 'verbose_name_plural': '评论内容'},
        ),
        migrations.AlterField(
            model_name='content',
            name='clicked',
            field=models.IntegerField(default=0, verbose_name='点击量'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='gender',
            field=models.CharField(choices=[('0', '男'), ('1', '女')], default='0', max_length=1, verbose_name='性别'),
        ),
    ]
