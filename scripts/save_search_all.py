#!/usr/bin/env python
import os
import sys

from django.core.exceptions import ValidationError

data_models = [('expenses','expense'),
    ]

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_repo.settings")
    os.environ["DJANGO_SETTINGS_MODULE"] = "site_repo.settings"
    
import django
django.setup()
from django.contrib.auth.models import User

all_models = User.objects.get(pk=1)._meta.apps.all_models
for app_label,model_name in data_models:
    model = all_models[app_label][model_name]
    if hasattr(model,'SearchConfig'):
        queryset = model.objects.all()
        for item in queryset:
            try:
                item.save()
            except ValidationError:
                pass