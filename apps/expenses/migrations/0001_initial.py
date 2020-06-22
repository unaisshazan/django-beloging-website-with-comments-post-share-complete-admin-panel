# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators
import site_repo.django_add.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_entered', models.DateTimeField(auto_now_add=True)),
                ('date_purchased', models.DateField()),
                ('month_balanced', models.IntegerField(validators=[site_repo.django_add.validators.verify_month_int])),
                ('year_balanced', models.IntegerField()),
                ('expense_sum', models.FloatField()),
                ('expense_divorcee_participate', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('desc', models.CharField(max_length=512)),
                ('slug', models.SlugField(max_length=128)),
                ('place_of_purchase', models.CharField(max_length=512)),
                ('notes', models.CharField(max_length=1024, blank=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('account', models.ForeignKey(related_name='expenses', to='accounts.Account')),
                ('owner', models.ForeignKey(related_name='expenses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
