from django import template
from django.template import Context, Template
from djangometrics.models import DjangoMetric

register = template.Library()

def get_for_site(context):
    site = context.get('site')
    return DjangoMetric.objects.get_for_site(site)


def get_for_model(context):
    model = context.get('object') or context.get('object_list')
    if model:
        return DjangoMetric.objects.get_for_model(model)
    return []


def _render(template, context):
    tpl = Template(template)
    ctx = Context(context)
    return tpl.render(ctx)


def get_tags(tagin, context):
    site_tags = [
            _render(getattr(tag, tagin), context) 
            for tag in get_for_site(context)
        ]

    model_tags = [
            _render(getattr(tag, tagin), context) 
            for tag in get_for_model(context)
        ]

    return {
        'site_tags': site_tags,
        'model_tags': model_tags,
    }


@register.inclusion_tag('djangometrics/tags.html', takes_context=True)
def tag_head_top(context):
    return get_tags('head_top', context)

@register.inclusion_tag('djangometrics/tags.html', takes_context=True)
def tag_head_bottom(context):
    return get_tags('head_bottom', context)

@register.inclusion_tag('djangometrics/tags.html', takes_context=True)
def tag_body_top(context):
    return get_tags('body_top', context)

@register.inclusion_tag('djangometrics/tags.html', takes_context=True)
def tag_body_bottom(context):
    return get_tags('body_bottom', context)
