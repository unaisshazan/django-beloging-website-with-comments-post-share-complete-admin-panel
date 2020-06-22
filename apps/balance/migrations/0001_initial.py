# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import site_repo.django_add.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyBalance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month_to_balance', models.IntegerField(validators=[site_repo.django_add.validators.verify_month_int])),
                ('year_to_balance', models.IntegerField()),
                ('is_balanced', models.BooleanField()),
                ('account', models.ForeignKey(related_name='months_balanced', to='accounts.Account')),
                ('divorcee1', models.ForeignKey(related_name='divorcee1_balance', blank=True, to=settings.AUTH_USER_MODEL)),
                ('divorcee2', models.ForeignKey(related_name='divorcee2_balance', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
