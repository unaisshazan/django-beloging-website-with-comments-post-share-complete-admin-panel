# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='divorcee2',
            field=models.ForeignKey(related_name='divorcee2_account', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
