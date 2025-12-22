import uuid

from django.conf import settings
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

        value = f"urn:maykin:test:{self.object.uuid}"
        result = field.to_internal_value(value)

        self.assertEqual(result, self.object)

    def test_validation(self):
        field_name = "uri"

        with self.subTest("required"):
            serializer = SerializerPlan(context={"request": None}, data={})
            serializer.is_valid()
            self.assertEqual(
                serializer.errors,
                {
                    field_name: [
                        ErrorDetail(
                            string="Dit veld is vereist.",
                            code="required",
                        )
                    ]
                },
            )

        with self.subTest("test incorrect_match uuid"):
            serializer = SerializerPlan(
                context={"request": None}, data={field_name: "urn:test:test:1234"}
            )
            serializer.is_valid()
            self.assertEqual(
                serializer.errors,
                {
                    field_name: [
                        ErrorDetail(
                            string="Invalid URI - Does not conform to the expected format.",
                            code="incorrect_match",
                        )
                    ]
                },
            )

        with self.subTest("test incorrect_type"):
            serializer = SerializerPlan(
                context={"request": None}, data={field_name: []}
            )
            serializer.is_valid()
            self.assertEqual(
                serializer.errors,
                {
                    field_name: [
                        ErrorDetail(
                            string=(
                                "Incorrect type. Expected a string representing a URI, "
                                "received list."
                            ),
                            code="incorrect_type",
                        )
                    ]
                },
            )

        with self.subTest("test invalid_urn_format"):
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

        with self.subTest("test invalid_url"):
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

        with self.subTest("test does_not_exist"):
            serializer = SerializerPlan(
                context={"request": None},
                data={field_name: f"urn:test:test:{uuid.uuid4()}"},
            )
            serializer.is_valid()
            self.assertEqual(
                serializer.errors,
                {
                    field_name: [
                        ErrorDetail(
                            string=(
                                "Invalid URI - Corresponding object does not exist."
                            ),
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

    def test_invalid_configuration(self):
        with self.subTest("test urn_component is None"):
            field = self.serializer.fields["uri"]

            # urn_component is None
            field.urn_component = None
            # request is None
            self.assertIsNone(self.serializer.context["request"])

            with self.assertRaises(ImproperlyConfigured) as error:
                field.to_representation(self.object)

            self.assertEqual(
                str(error.exception),
                "URIRelatedField could not determine the `urn_component`:"
                " request, resolver_match, or namespace is missing in serializer context.",
            )

            field.urn_component = "vtb"

        with self.subTest("test urn_resource is None"):
            field = self.serializer.fields["uri"]

            # urn_resource is None
            field.urn_resource = None
            # request is None
            self.assertIsNone(self.serializer.context["request"])

            with self.assertRaises(ImproperlyConfigured) as error:
                field.to_representation(self.object)

            self.assertEqual(
                str(error.exception),
                "URIRelatedField could not determine the `urn_resource`: "
                "model not found on the view or serializer.",
            )

            field.urn_resource = "test"

        with self.subTest("test no urn match"):
            field = self.serializer.fields["uri"]

            with self.assertRaises(ImproperlyConfigured) as error:
                new_object = ModelPlan(uuid=None)
                field.to_representation(new_object)

            self.assertEqual(
                str(error.exception),
                "Could not resolve URN for the object using the configured view."
                " You may have failed to include the related model in your API, or"
                " incorrectly configured the `urn_component` or `urn_resource` for this field.",
            )

    @override_settings(URN_NAMESPACE="")
    def test_empty_urn_namespace(self):
        self.assertEqual(settings.URN_NAMESPACE, "")

        with self.assertRaises(ImproperlyConfigured) as error:
            field = self.serializer.fields["uri"]
            field.to_representation(self.object)

        self.assertEqual(
            str(error.exception),
            "URIRelatedField requires a `urn_namespace` to be specified.",
        )

    def test_empty_urn_namespace_with_url(self):
        field = self.serializer.fields["uri"]
        url = "https://example.com/test"

        result = field.to_internal_value(url)
        self.assertEqual(result, url)
        representation = field.to_representation(url)
        self.assertEqual(representation, url)
