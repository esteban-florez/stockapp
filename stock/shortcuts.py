def session_errors(request):
  if request.session.get('errors'):
    errors_copy = request.session['errors'].copy()
    del request.session['errors']
    return errors_copy
  else:
    return None

def session_old(request):
  if request.session.get('old'):
    old_copy = request.session['old'].copy()
    del request.session['old']

    for key in ['category', 'product', 'supplier']:
      val = old_copy.get(key)
      if val:
        old_copy[key] = int(val)

    del old_copy['password']
    return old_copy
  else:
    return None
