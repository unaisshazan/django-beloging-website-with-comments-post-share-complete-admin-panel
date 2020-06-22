# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

# Adjust to your own DB such that search_text will support full text index
# Custom sql requires sqlparse (sudo pip install sqlparse)

# InnoDB supports full text from MySQL 5.7
MySQL_5_7 = """
CREATE TABLE `search_searchitems` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `object_name` varchar(255) NOT NULL,
    `search_text` varchar(1024) NOT NULL,
    `app_label` varchar(128) NOT NULL,
    `model_name` varchar(128) NOT NULL,
    `object_pk` integer NOT NULL,
    `object_account_id` integer NOT NULL,
    FULLTEXT KEY `name_info_search` (`object_name`,`search_text`)
    ) DEFAULT CHARSET=utf8
"""

# Befor MySQL 5.7, full text only with MyISAM
MySQL_5_6 = """
CREATE TABLE `search_searchitems` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `object_name` varchar(255) NOT NULL,
    `search_text` varchar(1024) NOT NULL,
    `app_label` varchar(128) NOT NULL,
    `model_name` varchar(128) NOT NULL,
    `object_pk` integer NOT NULL,
    `object_account_id` integer NOT NULL,
    FULLTEXT KEY `name_info_search` (`object_name`,`search_text`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8
"""

mig_sql = MySQL_5_6

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(sql=mig_sql,
                          reverse_sql="`search_searchitems`"),
    ]