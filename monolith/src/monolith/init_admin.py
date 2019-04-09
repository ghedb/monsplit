#!/usr/bin/env python
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monolith.settings")
django.setup()
from django.contrib.auth.models import User


if User.objects.count() == 0:
    User.objects.create_superuser('admin', 'admin@example.com', 'pass')
