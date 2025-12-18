from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.models.factories.plantype import PlanTypeFactory

from ...models.plantype import PlanType
from .api_testcase import APITestCase


class PlanTypeAPITests(APITestCase):
    def test_create_plantype(self):
        url = reverse("plannen_api:plantype-list")
        data = {"type": PlanTypeFactory.build().type}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        plantype = PlanType.objects.get(uuid=response.data["uuid"])
        self.assertEqual(plantype.type, data["type"])

    def test_list_plantypes(self):
        PlanTypeFactory.create_batch(3)

        url = reverse("plannen_api:plantype-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)
        for pt in data:
            self.assertIn("uuid", pt)
            self.assertIn("type", pt)

    def test_retrieve_plantype(self):
        plantype = PlanTypeFactory.create()
        url = reverse("plannen_api:plantype-detail", kwargs={"uuid": plantype.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(plantype.uuid))
        self.assertEqual(response.data["type"], plantype.type)

    def test_update_plantype(self):
        plantype = PlanTypeFactory.create()
        new_type = PlanTypeFactory.build().type

        url = reverse("plannen_api:plantype-detail", kwargs={"uuid": plantype.uuid})
        data = {"type": new_type}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plantype.refresh_from_db()
        self.assertEqual(plantype.type, new_type)

    def test_partial_update_plantype(self):
        plantype = PlanTypeFactory.create()
        new_type = PlanTypeFactory.build().type

        url = reverse("plannen_api:plantype-detail", kwargs={"uuid": plantype.uuid})
        data = {"type": new_type}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plantype.refresh_from_db()
        self.assertEqual(plantype.type, new_type)

    def test_delete_plantype(self):
        plantype = PlanTypeFactory.create()
        url = reverse("plannen_api:plantype-detail", kwargs={"uuid": plantype.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PlanType.objects.filter(uuid=plantype.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen_api:plan-list")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_plantype_by_type(self):
        plantype_match = PlanTypeFactory.create(type="pip")
        PlanTypeFactory.create(type="werk")
        PlanTypeFactory.create(type="inkomen")

        url = reverse("plannen_api:plantype-list")
        response = self.client.get(url, {"type": "pip"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["uuid"], str(plantype_match.uuid))
        self.assertEqual(data["results"][0]["type"], "pip")
