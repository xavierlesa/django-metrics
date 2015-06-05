# -*- coding:utf-8 -*-

from django.contrib import admin
from djangometrics.models import DjangoMetric

class DjangoMetricAdmin(admin.ModelAdmin):
    list_display = (
            'tag_name',
            'content_type',
            'object_id',
            )
admin.site.register(DjangoMetric, DjangoMetricAdmin)
