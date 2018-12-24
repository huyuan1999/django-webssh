#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : HuYuan
# @File    : tools.py

from django import forms


class ValidationData(forms.Form):
    host = forms.CharField(max_length=32)
    port = forms.IntegerField()
    user = forms.CharField(max_length=32)
    auth = forms.CharField(max_length=16)
    pkey = forms.FileField(required=False)
    password = forms.CharField(max_length=180, required=False)
    width = forms.IntegerField()
    height = forms.IntegerField()