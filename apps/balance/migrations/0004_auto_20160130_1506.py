# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0003_auto_20160129_1512'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='monthlybalance',
            unique_together=set([('month_of_balance', 'year_of_balance', 'account')]),
        ),
    ]
