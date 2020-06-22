# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_auto_20160128_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='account',
            field=models.ForeignKey(related_name='expenses', blank=True, to='accounts.Account', null=True),
        ),
    ]
