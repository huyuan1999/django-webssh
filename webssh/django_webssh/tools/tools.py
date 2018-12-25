#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : HuYuan
# @File    : tools.py

from django import forms
from django_webssh import models
import time
import random
import hashlib



class ValidationData(forms.ModelForm):
    class Meta:
        model = models.HostTmp
        exclude = ['datetime']


def unique():
    ctime = str(time.time())
    salt = str(random.random())
    m = hashlib.md5(bytes(salt, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

