# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlybalance',
            name='divorcee1',
            field=models.ForeignKey(related_name='divorcee1_balance', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='monthlybalance',
            name='divorcee2',
            field=models.ForeignKey(related_name='divorcee2_balance', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
