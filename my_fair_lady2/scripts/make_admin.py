#!/usr/bin/env python
import os

from django.contrib.auth.models import User
if User.objects.count() == 0:
    admin = User.objects.create(username='admin')
    admin.set_password(os.environ['DJANGO_ADMIN_SU_PASSWORD'])
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
