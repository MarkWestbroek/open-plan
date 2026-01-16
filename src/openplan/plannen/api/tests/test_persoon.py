from unittest.mock import MagicMock, patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.metrics import (
    personen_create_counter,
    personen_delete_counter,
    personen_update_counter,
)
from openplan.plannen.models.factories.persoon import PersoonFactory

from ...models.persoon import Persoon
from .api_testcase import APITestCase


class PersoonAPITests(APITestCase):
    def test_create_persoon(self):
        url = reverse("plannen:persoon-list")
        data = {
            "persoonsprofiel": "urn:example:persoon:12345",
            "klant": "urn:example:klant:67890",
            "bsn": "963773215",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        persoon = Persoon.objects.get(uuid=response.data["uuid"])
        self.assertEqual(persoon.persoonsprofiel, data["persoonsprofiel"])
        self.assertEqual(persoon.klant, data["klant"])
        self.assertEqual(persoon.bsn, data["bsn"])

    def test_list_personen(self):
        PersoonFactory.create_batch(3)

        url = reverse("plannen:persoon-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)
        for p in data:
            self.assertIn("uuid", p)
            self.assertIn("persoonsprofiel", p)
            self.assertIn("klant", p)
            self.assertIn("bsn", p)

    def test_retrieve_persoon(self):
        persoon = PersoonFactory.create()
        url = reverse("plannen:persoon-detail", kwargs={"uuid": persoon.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(persoon.uuid))
        self.assertEqual(response.data["persoonsprofiel"], persoon.persoonsprofiel)
        self.assertEqual(response.data["klant"], persoon.klant)
        self.assertEqual(response.data["bsn"], persoon.bsn)

    def test_update_persoon(self):
        persoon = PersoonFactory.create()
        new_data = {
            "persoonsprofiel": "urn:example:persoon:12345",
            "klant": "urn:example:klant:67890",
            "bsn": "111222333",
        }
        url = reverse("plannen:persoon-detail", kwargs={"uuid": persoon.uuid})
        response = self.client.put(url, new_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        persoon.refresh_from_db()
        self.assertEqual(persoon.persoonsprofiel, new_data["persoonsprofiel"])
        self.assertEqual(persoon.klant, new_data["klant"])
        self.assertEqual(persoon.bsn, new_data["bsn"])

    def test_partial_update_persoon(self):
        persoon = PersoonFactory.create()
        new_data = {"bsn": "111222333"}
        url = reverse("plannen:persoon-detail", kwargs={"uuid": persoon.uuid})
        response = self.client.patch(url, new_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        persoon.refresh_from_db()
        self.assertEqual(persoon.bsn, new_data["bsn"])

    def test_delete_persoon(self):
        persoon = PersoonFactory.create()
        url = reverse("plannen:persoon-detail", kwargs={"uuid": persoon.uuid})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Persoon.objects.filter(uuid=persoon.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen:persoon-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch.object(personen_create_counter, "add", wraps=personen_create_counter.add)
    def test_create_persoon_increments_metric(self, mock_add: MagicMock):
        url = reverse("plannen:persoon-list")
        data = {
            "persoonsprofiel": "urn:example:persoon:12345",
            "klant": "urn:example:klant:67890",
            "bsn": "963773215",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        mock_add.assert_called_once_with(1)

    @patch.object(personen_update_counter, "add", wraps=personen_update_counter.add)
    def test_update_persoon_increments_metric(self, mock_add: MagicMock):
        persoon = PersoonFactory.create()
        new_data = {"bsn": "111222333"}
        url = reverse("plannen:persoon-detail", kwargs={"uuid": persoon.uuid})
        response = self.client.patch(url, new_data, format="json")
        self.assertEqual(response.status_code, 200)
        mock_add.assert_called_once_with(1)

    @patch.object(personen_delete_counter, "add", wraps=personen_delete_counter.add)
    def test_delete_persoon_increments_metric(self, mock_add: MagicMock):
        persoon = PersoonFactory.create()
        url = reverse("plannen:persoon-detail", kwargs={"uuid": persoon.uuid})
        response = self.client.delete(url)
        self.assertIn(response.status_code, (200, 204))
        mock_add.assert_called_once_with(1)
