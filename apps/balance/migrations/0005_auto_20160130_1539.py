# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0004_auto_20160130_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlybalance',
            name='is_balanced',
            field=models.BooleanField(default=False),
        ),
    ]
