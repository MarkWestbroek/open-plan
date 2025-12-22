from django.conf import settings
from django.utils.translation import gettext_lazy as _

description = _("""
Een API voor Plannen.
""")

custom_settings = {
    "TITLE": "Plannen API",
    "VERSION": settings.PLANNEN_API_VERSION,
    "DESCRIPTION": description,
    "SERVERS": [{"url": f"/plannen/api/v{settings.API_VERSION}"}],
}
