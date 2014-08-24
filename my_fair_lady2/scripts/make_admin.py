#!/usr/bin/env python

from my_fair_lady.settings.production import get_env_setting
from django.contrib.auth.models import User
if User.objects.count() == 0:
    admin = User.objects.create(username='admin')
    admin.set_password(get_env_setting('DJANGO_ADMIN_SU_PASSWORD'))
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
