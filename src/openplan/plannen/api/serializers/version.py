from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from openplan.plannen.models.version import Version


class VersionSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {"plan_uuid": "plan__uuid"}

    class Meta:
        model = Version
        fields = [
            "url",
            "version",
            "plan",
            "actor",
            "comment",
            "created_at",
            "snapshot",
        ]
        extra_kwargs = {
            "url": {"lookup_field": "version"},
            "version": {"read_only": True},
        }
