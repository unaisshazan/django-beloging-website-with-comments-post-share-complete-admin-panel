# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_name', models.CharField(max_length=255)),
                ('search_text', models.CharField(max_length=1024)),
                ('app_label', models.CharField(max_length=128)),
                ('model_name', models.CharField(max_length=128)),
                ('object_pk', models.IntegerField()),
            ],
            options={
                'db_table': 'search_searchitems',
                'managed': False,
            },
        ),
    ]
