import datetime
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def value(context, model, prop):
  if model:
    return getattr(model, prop)
  old = context.get('old')
  if old:
    val = old.get(prop)
    return val if val else ''

  return ''
