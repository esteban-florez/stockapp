from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def value(context, model, prop):
  old = context.get('old')
  value = ''

  if old and old.get(prop):
    value = old.get(prop)
  elif model:
    value = getattr(model, prop)

  return value
  
@register.simple_tag(takes_context=True)
def selected(context, model, prop, value):
  old = context.get('old')
  match = False

  if old and old.get(prop):
    match = int(old.get(prop)) == value
  elif model:
    match = getattr(model, prop).id == value

  return 'selected' if match else ''
