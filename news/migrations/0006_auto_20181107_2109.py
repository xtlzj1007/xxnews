# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-07 13:09
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20181106_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='content',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='', verbose_name='新闻内容'),
            preserve_default=False,
        ),
    ]
