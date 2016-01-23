# Custom template context processors

from .config import SITE_CONFIG


def site_config_processor(request):
    """Context processor to make SITE_CONFIG available to all templates."""

    return {'SITE_CONFIG': SITE_CONFIG}
