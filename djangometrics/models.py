# -*- coding:utf8 -*-

from django.db import models
try:
    from django.contrib.contenttypes.generic import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.query import EmptyQuerySet
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
import collections


class DjangoMetricManager(models.Manager):
    def get_for_model(self, model, *args, **kwargs):
        try:
            if isinstance(model, models.QuerySet):
                model = model.model
            elif not isinstance(model, models.Model):
                return [] 
        except AttributeError:
            if isinstance(model, collections.Iterable):
                model = model.model

        ct = ContentType.objects.get_for_model(model)

        try:
            qs = self.get_query_set
        except:
            qs = self.get_queryset

        qs = qs(*args, **kwargs).filter(content_type=ct)

        if hasattr(model, 'id') and getattr(model, 'id'):
            qs = qs.filter(object_id=model.id)

        return qs

    def get_for_site(self, sites, *args, **kwargs):
        if not isinstance(sites, collections.Iterable):
            sites = [sites]

        try:
            qs = self.get_query_set
        except:
            qs = self.get_queryset

        return qs(*args, **kwargs).filter(
                models.Q(sites__in = sites) | models.Q(sites__isnull = True),
                content_type__isnull = True, object_id__isnull = True
            )



class DjangoMetric(models.Model):

    TAG_TYPE_CHOICES = (
        ('google-analitycs', 'Google Analytics'),
        ('crazy-egg', 'Crazy Egg'),
        ('facebook', 'Facebook'),
        ('google-ads-convertion', 'Google Ads Convertion'),
        ('facebook-ads-convertion', 'Facebook Ads Convertion'),
        ('other', 'Otro'),
    )

    TAG = "<!-- %(tag_name)s // %(tag_type)s -->\n%(tag)s\n<!-- END %(tag_name)s TAG -->"

    tag_name = models.CharField(max_length=100)
    tag_type = models.CharField(max_length=100, choices=TAG_TYPE_CHOICES)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    sites = models.ManyToManyField(Site, blank=True, null=True)
    tag_head_top = models.TextField(blank=True, null=True, help_text="Tags a incluir al iniciar el tag HEAD")
    tag_head_bottom = models.TextField(blank=True, null=True, help_text="Tags a incluir al final del tag HEAD")
    tag_body_top = models.TextField(blank=True, null=True, help_text="Tags a incluir al inicio del tag BODY")
    tag_body_bottom = models.TextField(blank=True, null=True, help_text="Tags a incluir al final del tag BODY")

    objects = DjangoMetricManager()

    def __unicode__(self):
        return self.tag_name

    @property
    def head_top(self):
        if not self.tag_head_top:
            return ''

        return mark_safe(self.TAG % dict(
            tag_name=self.tag_name, 
            tag_type=self.tag_type, 
            tag=self.tag_head_top
            )
        )

    @property
    def head_bottom(self):
        if not self.tag_head_bottom:
            return ''

        return mark_safe(self.TAG % dict(
            tag_name=self.tag_name, 
            tag_type=self.tag_type, 
            tag=self.tag_head_bottom
            )
        )

    @property
    def body_top(self):
        if not self.tag_body_top:
            return ''

        return mark_safe(self.TAG % dict(
            tag_name=self.tag_name, 
            tag_type=self.tag_type, 
            tag=self.tag_body_top
            )
        )

    @property
    def body_bottom(self):
        if not self.tag_body_bottom:
            return ''

        return mark_safe(self.TAG % dict(
            tag_name=self.tag_name, 
            tag_type=self.tag_type, 
            tag=self.tag_body_bottom
            )
        )
