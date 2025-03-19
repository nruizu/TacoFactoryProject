#Autor: Nicolas Ruiz
def base_template(request):
    if request.user.is_authenticated:
        return {'base_template': 'base_loged.html'}
    return {'base_template': 'base.html'}