# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import site_repo.django_add.validators


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_auto_20160128_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date_entered',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'Entered On'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date_purchased',
            field=models.DateField(verbose_name=b'Date of Purchase'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='desc',
            field=models.CharField(max_length=512, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='expense_divorcee_participate',
            field=models.IntegerField(verbose_name=b'Divorcee participate %', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='expense',
            name='expense_sum',
            field=models.FloatField(verbose_name=b'Cost'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name=b'Approved?'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='month_balanced',
            field=models.IntegerField(choices=[(1, b'Jan'), (2, b'Feb'), (3, b'Mar'), (4, b'Apr'), (5, b'May'), (6, b'Jun'), (7, b'Jul'), (8, b'Aug'), (9, b'Sep'), (10, b'Oct'), (11, b'Nov'), (12, b'Dec')], verbose_name=b'Balance on month', validators=[site_repo.django_add.validators.verify_month_int]),
        ),
        migrations.AlterField(
            model_name='expense',
            name='notes',
            field=models.CharField(max_length=1024, verbose_name=b'Notes', blank=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='place_of_purchase',
            field=models.CharField(max_length=512, verbose_name=b'Place of purchase'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='year_balanced',
            field=models.IntegerField(verbose_name=b'Balance on year', choices=[(2016, 2016), (2017, 2017)]),
        ),
    ]
