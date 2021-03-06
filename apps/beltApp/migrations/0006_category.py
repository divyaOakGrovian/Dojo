# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-22 21:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beltApp', '0005_auto_20190722_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('job', models.ManyToManyField(related_name='categories', to='beltApp.Job')),
            ],
        ),
    ]
