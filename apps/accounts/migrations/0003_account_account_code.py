# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import site_repo.apps.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20160128_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_code',
            field=models.CharField(default=site_repo.apps.accounts.models.default_account_code, max_length=36),
        ),
    ]
