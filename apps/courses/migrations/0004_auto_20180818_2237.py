# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-18 22:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_remove_course_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='learn_times',
        ),
        migrations.AlterField(
            model_name='video',
            name='learn_times',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='学习时长(分钟数)'),
        ),
    ]
