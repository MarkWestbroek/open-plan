from unittest.mock import MagicMock, patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.metrics import (
    contactmomenten_create_counter,
    contactmomenten_delete_counter,
    contactmomenten_update_counter,
)
from openplan.plannen.models.factories.contactmoment import ContactmomentFactory
from openplan.plannen.models.factories.plan import PlanFactory

from ...models.contactmoment import Contactmoment
from .api_testcase import APITestCase


class ContactmomentAPITests(APITestCase):
    def test_create_contactmoment(self):
        plan = PlanFactory.create()
        url = reverse("plannen:contactmoment-list")
        data = {"plan_uuid": str(plan.uuid)}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contactmoment = Contactmoment.objects.get(uuid=response.data["uuid"])
        self.assertEqual(contactmoment.plan, plan)

    def test_list_contactmomenten(self):
        ContactmomentFactory.create_batch(3)

        url = reverse("plannen:contactmoment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)
        for cm in data:
            self.assertIn("uuid", cm)
            self.assertIn("plan", cm)

    def test_retrieve_contactmoment(self):
        contactmoment = ContactmomentFactory.create()
        url = reverse(
            "plannen:contactmoment-detail", kwargs={"uuid": contactmoment.uuid}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(contactmoment.uuid))
        self.assertEqual(response.data["plan"]["uuid"], str(contactmoment.plan.uuid))

    def test_update_contactmoment(self):
        contactmoment = ContactmomentFactory.create()
        new_plan = PlanFactory.create()

        url = reverse(
            "plannen:contactmoment-detail", kwargs={"uuid": contactmoment.uuid}
        )
        data = {"plan_uuid": str(new_plan.uuid)}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contactmoment.refresh_from_db()
        self.assertEqual(contactmoment.plan, new_plan)

    def test_partial_update_contactmoment(self):
        contactmoment = ContactmomentFactory.create()
        new_plan = PlanFactory.create()

        url = reverse(
            "plannen:contactmoment-detail", kwargs={"uuid": contactmoment.uuid}
        )
        data = {"plan_uuid": str(new_plan.uuid)}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contactmoment.refresh_from_db()
        self.assertEqual(contactmoment.plan, new_plan)

    def test_delete_contactmoment(self):
        contactmoment = ContactmomentFactory.create()
        url = reverse(
            "plannen:contactmoment-detail", kwargs={"uuid": contactmoment.uuid}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contactmoment.objects.filter(uuid=contactmoment.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen:contactmoment-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch.object(
        contactmomenten_create_counter, "add", wraps=contactmomenten_create_counter.add
    )
    def test_create_contactmoment_increments_metric(self, mock_add: MagicMock):
        plan = PlanFactory.create()
        url = reverse("plannen:contactmoment-list")
        data = {"plan_uuid": str(plan.uuid)}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        mock_add.assert_called_once_with(1)

    @patch.object(
        contactmomenten_update_counter, "add", wraps=contactmomenten_update_counter.add
    )
    def test_update_contactmoment_increments_metric(self, mock_add: MagicMock):
        contactmoment = ContactmomentFactory.create()
        new_plan = PlanFactory.create()
        url = reverse(
            "plannen:contactmoment-detail", kwargs={"uuid": contactmoment.uuid}
        )
        data = {"plan_uuid": str(new_plan.uuid)}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        mock_add.assert_called_once_with(1)

    @patch.object(
        contactmomenten_delete_counter, "add", wraps=contactmomenten_delete_counter.add
    )
    def test_delete_contactmoment_increments_metric(self, mock_add: MagicMock):
        contactmoment = ContactmomentFactory.create()
        url = reverse(
            "plannen:contactmoment-detail", kwargs={"uuid": contactmoment.uuid}
        )
        response = self.client.delete(url)
        self.assertIn(response.status_code, (200, 204))
        mock_add.assert_called_once_with(1)
