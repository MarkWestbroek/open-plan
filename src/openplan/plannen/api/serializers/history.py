# openplan/plannen/api/serializers/history.py
from rest_framework import serializers


class HistoryEventSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField(source="pgh_created_at")
    action = serializers.CharField(source="pgh_label")
    model = serializers.SerializerMethodField()
    object_id = serializers.SerializerMethodField()
    data = serializers.DictField()

    def get_model(self, obj):
        return obj._meta.label_lower

    def get_object_id(self, obj):
        return getattr(obj, "pgh_obj_id", None)

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        payload = {}
        for field in instance._meta.fields:
            name = field.name
            if name.startswith("pgh_"):
                continue
            if name in ("id",):
                continue
            payload[name] = getattr(instance, name)

        rep["data"] = payload
        return rep
