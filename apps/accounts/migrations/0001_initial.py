# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('divorcee1', models.ForeignKey(related_name='divorcee1_account', to=settings.AUTH_USER_MODEL)),
                ('divorcee2', models.ForeignKey(related_name='divorcee2_account', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
