from django.conf import settings as django_settings

def settings(request):
    """ Exposes some project settings in template context

    Exposed as a dict under `settings` template var.
    """
    d =  {
        'settings': {k: getattr(django_settings, k, '')
                     for k in django_settings.TEMPLATE_SETTINGS}
    }
    return d
