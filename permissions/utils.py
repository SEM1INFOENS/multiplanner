
def get_default_permission_name(model, perm_name):
    ''' returns the default permission name (view, change, add or delete)
    for a particular model
    these permissions are automaticaly created with the migrations '''
    s = model._meta.label_lower.split('.')
    model_name = s.pop()
    app_name = '.'.join(s)
    return app_name+'.'+perm_name+'_'+model_name
