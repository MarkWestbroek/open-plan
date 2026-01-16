from unittest.mock import MagicMock, patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.metrics import (
    relatietypen_create_counter,
    relatietypen_delete_counter,
    relatietypen_update_counter,
)
from openplan.plannen.models.factories.relatietype import RelatieTypeFactory

from ...models.relatietype import RelatieType
from .api_testcase import APITestCase


class RelatieTypeAPITests(APITestCase):
    def test_create_relatietype(self):
        url = reverse("plannen:relatietype-list")
        data = {"naam": RelatieTypeFactory.build().naam}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        relatietype = RelatieType.objects.get(uuid=response.data["uuid"])
        self.assertEqual(relatietype.naam, data["naam"])

    def test_list_relatietypes(self):
        RelatieTypeFactory.create_batch(3)

        url = reverse("plannen:relatietype-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)
        for rt in data:
            self.assertIn("uuid", rt)
            self.assertIn("naam", rt)

    def test_retrieve_relatietype(self):
        relatietype = RelatieTypeFactory.create()
        url = reverse("plannen:relatietype-detail", kwargs={"uuid": relatietype.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(relatietype.uuid))
        self.assertEqual(response.data["naam"], relatietype.naam)

    def test_update_relatietype(self):
        relatietype = RelatieTypeFactory.create()
        new_naam = RelatieTypeFactory.build().naam

        url = reverse("plannen:relatietype-detail", kwargs={"uuid": relatietype.uuid})
        data = {"naam": new_naam}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        relatietype.refresh_from_db()
        self.assertEqual(relatietype.naam, new_naam)

    def test_partial_update_relatietype(self):
        relatietype = RelatieTypeFactory.create()
        new_naam = RelatieTypeFactory.build().naam

        url = reverse("plannen:relatietype-detail", kwargs={"uuid": relatietype.uuid})
        data = {"naam": new_naam}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        relatietype.refresh_from_db()
        self.assertEqual(relatietype.naam, new_naam)

    def test_delete_relatietype(self):
        relatietype = RelatieTypeFactory.create()
        url = reverse("plannen:relatietype-detail", kwargs={"uuid": relatietype.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RelatieType.objects.filter(uuid=relatietype.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen:relatietype-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_relatietype_by_naam(self):
        relatietype_match = RelatieTypeFactory.create(naam="Collega")
        RelatieTypeFactory.create(naam="Familie")
        RelatieTypeFactory.create(naam="Vriend")

        url = reverse("plannen:relatietype-list")
        response = self.client.get(url, {"naam": "Collega"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["uuid"], str(relatietype_match.uuid))
        self.assertEqual(data["results"][0]["naam"], "Collega")

    @patch.object(
        relatietypen_create_counter, "add", wraps=relatietypen_create_counter.add
    )
    def test_create_relatietype_increments_metric(self, mock_add: MagicMock):
        url = reverse("plannen:relatietype-list")
        data = {"naam": RelatieTypeFactory.build().naam}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        mock_add.assert_called_once_with(1)

    @patch.object(
        relatietypen_update_counter, "add", wraps=relatietypen_update_counter.add
    )
    def test_update_relatietype_increments_metric(self, mock_add: MagicMock):
        relatietype = RelatieTypeFactory.create()
        new_naam = RelatieTypeFactory.build().naam

        url = reverse("plannen:relatietype-detail", kwargs={"uuid": relatietype.uuid})
        data = {"naam": new_naam}

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        mock_add.assert_called_once_with(1)

    @patch.object(
        relatietypen_delete_counter, "add", wraps=relatietypen_delete_counter.add
    )
    def test_delete_relatietype_increments_metric(self, mock_add: MagicMock):
        relatietype = RelatieTypeFactory.create()

        url = reverse("plannen:relatietype-detail", kwargs={"uuid": relatietype.uuid})
        response = self.client.delete(url)
        self.assertIn(response.status_code, (200, 204))
        mock_add.assert_called_once_with(1)
