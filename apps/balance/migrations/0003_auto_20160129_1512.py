# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0002_auto_20160129_1401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monthlybalance',
            old_name='month_to_balance',
            new_name='month_of_balance',
        ),
        migrations.RenameField(
            model_name='monthlybalance',
            old_name='year_to_balance',
            new_name='year_of_balance',
        ),
    ]
