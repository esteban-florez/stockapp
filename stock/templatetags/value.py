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
  
@register.simple_tag(takes_context=True)
def selected(context, model, prop, value):
  old = context.get('old')
  match = False

  if old and old.get(prop):
    match = int(old.get(prop)) == value
  elif model:
    match = getattr(model, prop).id == value

  return 'selected' if match else ''
