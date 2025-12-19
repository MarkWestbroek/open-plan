import uuid

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.test import override_settings

from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from openplan.utils.serializers import URIRelatedField


class ModelPlan:
    def __init__(self, uuid):
        self.uuid = uuid


class QuerySetPlan:
    def __init__(self, objects, lookup_field):
        self.objects = objects
        self.lookup_field = lookup_field

    def get(self, **kwargs):
        key, value = list(kwargs.items())[0]
        for obj in self.objects:
            if str(getattr(obj, key)) == value:
                return obj
        raise ObjectDoesNotExist()


class SerializerPlan(serializers.Serializer):
    uri = URIRelatedField(
        view_name="plan:test-detail",
        urn_component="plan",
        urn_resource="test",
        lookup_field="uuid",
        required=True,
        queryset=QuerySetPlan([], lookup_field="uuid"),
    )


class URIFieldTest(APITestCase):
    def setUp(self):
        self.object = ModelPlan(uuid=uuid.uuid4())
        self.serializer = SerializerPlan(
            instance=self.object, context={"request": None}
        )

    def test_to_representation(self):
        field = self.serializer.fields["uri"]

        urn = field.to_representation(self.object)

        self.assertEqual(urn, f"urn:maykin:plan:test:{str(self.object.uuid)}")

    def test_to_internal_value(self):
        field = self.serializer.fields["uri"]
        field.get_queryset = lambda: QuerySetPlan([self.object], lookup_field="uuid")

        value = f"urn:maykin:plan:test:{self.object.uuid}"
        result = field.to_internal_value(value)

        self.assertEqual(result, self.object)

    def test_validation(self):
        field_name = "uri"

        # required
        serializer = SerializerPlan(context={"request": None}, data={})
        serializer.is_valid()
        self.assertEqual(
            serializer.errors,
            {field_name: [ErrorDetail(string="Dit veld is vereist.", code="required")]},
        )

        # invalid type
        serializer = SerializerPlan(context={"request": None}, data={field_name: []})
        serializer.is_valid()
        self.assertEqual(
            serializer.errors,
            {
                field_name: [
                    ErrorDetail(
                        string="Incorrect type. Expected a string representing a URI, received list.",
                        code="incorrect_type",
                    )
                ]
            },
        )

        # invalid URN format
        serializer = SerializerPlan(
            context={"request": None}, data={field_name: "urn:test"}
        )
        serializer.is_valid()
        self.assertEqual(
            serializer.errors,
            {
                field_name: [
                    ErrorDetail(
                        string="Invalid URI - Could not match the expected pattern.",
                        code="no_match",
                    )
                ]
            },
        )

        # invalid URL
        serializer = SerializerPlan(
            context={"request": None}, data={field_name: "ftp://example.com"}
        )
        serializer.is_valid()
        self.assertEqual(
            serializer.errors,
            {
                field_name: [
                    ErrorDetail(
                        string="Invalid URI - Could not match the expected pattern.",
                        code="no_match",
                    )
                ]
            },
        )

        # non-existent URN object
        serializer = SerializerPlan(
            context={"request": None},
            data={field_name: f"urn:maykin:plan:test:{uuid.uuid4()}"},
        )
        serializer.is_valid()
        self.assertEqual(
            serializer.errors,
            {
                field_name: [
                    ErrorDetail(
                        string="Invalid URI - Corresponding object does not exist..",
                        code="does_not_exist",
                    )
                ]
            },
        )

    def test_valid_urls(self):
        field = self.serializer.fields["uri"]

        valid_urls = [
            "http://example.com",
            "https://example.com/path?query=123",
            "https://sub.domain.com/resource",
        ]

        for url in valid_urls:
            result = field.to_internal_value(url)
            self.assertEqual(result, url)

            representation = field.to_representation(url)
            self.assertEqual(representation, url)

    @override_settings(URN_NAMESPACE="")
    def test_empty_urn_namespace(self):
        with self.assertRaises(ImproperlyConfigured) as error:
            field = self.serializer.fields["uri"]
            field.to_representation(self.object)

        self.assertEqual(
            str(error.exception),
            "URIRelatedField requires a `urn_namespace` to be specified.",
        )

    @override_settings(URN_NAMESPACE="")
    def test_empty_urn_namespace_with_url(self):
        field = self.serializer.fields["uri"]
        url = "https://example.com/test"

        result = field.to_internal_value(url)
        self.assertEqual(result, url)
        representation = field.to_representation(url)
        self.assertEqual(representation, url)
