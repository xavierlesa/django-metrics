# -*- coding:utf-8 -*-

from django.contrib import admin
from djangometrics.models import DjangoMetric

class DjangoMetricAdmin(admin.ModelAdmin):
    pass
admin.site.register(DjangoMetric, DjangoMetricAdmin)
