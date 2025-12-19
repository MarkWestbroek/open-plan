from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .validators import URIValidator


class URIField(models.CharField):
    """
    A Django model field for Uniform Resource Identifiers (RFC 3986),
    supporting both URLs and URNs.
    """

    default_validators = [URIValidator()]
    description = _("URI")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 500)
        super().__init__(*args, **kwargs)


@extend_schema_field(OpenApiTypes.UUID)
class UUIDRelatedField(serializers.RelatedField):
    """
    A read-write field that represents the target of the relationship
    by a unique 'uuid' attribute.
    """

    default_error_messages = {
        "does_not_exist": _("Object with uuid={value} does not exist."),
        "invalid": _("Invalid value."),
    }

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get(uuid=data)
        except ObjectDoesNotExist:
            self.fail("does_not_exist", value=smart_str(data))
        except (TypeError, ValueError):
            self.fail("invalid")

    def to_representation(self, obj):
        return str(obj.uuid)
