from django.urls import reverse

from rest_framework import status

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
