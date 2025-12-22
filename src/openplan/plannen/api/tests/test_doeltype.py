from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.models.factories.doeltype import DoelTypeFactory

from ...models.doeltype import DoelType
from .api_testcase import APITestCase


class DoelTypeAPITests(APITestCase):
    def test_create_doeltype(self):
        url = reverse("plannen:doeltype-list")
        data = {"type": DoelTypeFactory.build().type}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        doeltype = DoelType.objects.get(uuid=response.data["uuid"])
        self.assertEqual(doeltype.type, data["type"])

    def test_list_doeltypes(self):
        DoelTypeFactory.create_batch(3)

        url = reverse("plannen:doeltype-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)
        for dt in data:
            self.assertIn("uuid", dt)
            self.assertIn("type", dt)

    def test_retrieve_doeltype(self):
        doeltype = DoelTypeFactory.create()
        url = reverse("plannen:doeltype-detail", kwargs={"uuid": doeltype.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(doeltype.uuid))
        self.assertEqual(response.data["type"], doeltype.type)

    def test_update_doeltype(self):
        doeltype = DoelTypeFactory.create()
        new_type = DoelTypeFactory.build().type

        url = reverse("plannen:doeltype-detail", kwargs={"uuid": doeltype.uuid})
        data = {"type": new_type}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        doeltype.refresh_from_db()
        self.assertEqual(doeltype.type, new_type)

    def test_partial_update_doeltype(self):
        doeltype = DoelTypeFactory.create()
        new_type = DoelTypeFactory.build().type

        url = reverse("plannen:doeltype-detail", kwargs={"uuid": doeltype.uuid})
        data = {"type": new_type}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        doeltype.refresh_from_db()
        self.assertEqual(doeltype.type, new_type)

    def test_delete_doeltype(self):
        doeltype = DoelTypeFactory.create()
        url = reverse("plannen:doeltype-detail", kwargs={"uuid": doeltype.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DoelType.objects.filter(uuid=doeltype.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen:doeltype-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_doeltype_by_type(self):
        doeltype_match = DoelTypeFactory.create(type="hoofddoel")
        DoelTypeFactory.create(type="werk")
        DoelTypeFactory.create(type="inkomen")

        url = reverse("plannen:doeltype-list")
        response = self.client.get(url, {"type": "hoofddoel"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["uuid"], str(doeltype_match.uuid))
        self.assertEqual(data["results"][0]["type"], "hoofddoel")
