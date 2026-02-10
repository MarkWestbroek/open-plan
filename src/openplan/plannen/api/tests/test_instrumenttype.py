from unittest.mock import MagicMock, patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.metrics import (
    instrumenttypen_create_counter,
    instrumenttypen_delete_counter,
    instrumenttypen_update_counter,
)
from openplan.plannen.models.factories.instrumentcategorie import (
    InstrumentCategorieFactory,
)
from openplan.plannen.models.factories.instrumenttype import InstrumenttypeFactory

from ...models.instrumenttype import InstrumentType
from .api_testcase import APITestCase


class InstrumentTypeAPITests(APITestCase):
    def setUp(self):
        super().setUp()
        self.categorie = InstrumentCategorieFactory.create()

    def test_create_instrumenttype(self):
        url = reverse("plannen:instrumenttype-list")
        data = {
            "instrument_type": InstrumenttypeFactory.build().instrument_type,
            "categorieen_uuids": [str(self.categorie.uuid)],
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        instrumenttype = InstrumentType.objects.get(uuid=response.data["uuid"])
        self.assertEqual(instrumenttype.instrument_type, data["instrument_type"])

    def test_list_instrumenttypes(self):
        InstrumenttypeFactory.create_batch(3)

        url = reverse("plannen:instrumenttype-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)
        for it in data:
            self.assertIn("uuid", it)
            self.assertIn("instrumentType", it)

    def test_retrieve_instrumenttype(self):
        instrumenttype = InstrumenttypeFactory.create()
        url = reverse(
            "plannen:instrumenttype-detail", kwargs={"uuid": instrumenttype.uuid}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(instrumenttype.uuid))
        self.assertEqual(
            response.data["instrument_type"], instrumenttype.instrument_type
        )

    def test_update_instrumenttype(self):
        instrumenttype = InstrumenttypeFactory.create()
        new_type = InstrumenttypeFactory.build().instrument_type

        url = reverse(
            "plannen:instrumenttype-detail", kwargs={"uuid": instrumenttype.uuid}
        )
        data = {
            "instrument_type": new_type,
            "categorieen_uuids": [str(self.categorie.uuid)],
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        instrumenttype.refresh_from_db()
        self.assertEqual(instrumenttype.instrument_type, new_type)

    def test_partial_update_instrumenttype(self):
        instrumenttype = InstrumenttypeFactory.create()
        new_type = InstrumenttypeFactory.build().instrument_type

        url = reverse(
            "plannen:instrumenttype-detail", kwargs={"uuid": instrumenttype.uuid}
        )
        data = {"instrument_type": new_type}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        instrumenttype.refresh_from_db()
        self.assertEqual(instrumenttype.instrument_type, new_type)

    def test_delete_instrumenttype(self):
        instrumenttype = InstrumenttypeFactory.create()
        url = reverse(
            "plannen:instrumenttype-detail", kwargs={"uuid": instrumenttype.uuid}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            InstrumentType.objects.filter(uuid=instrumenttype.uuid).exists()
        )

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen:instrumenttype-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch.object(
        instrumenttypen_create_counter, "add", wraps=instrumenttypen_create_counter.add
    )
    def test_create_instrumenttype_increments_metric(self, mock_add: MagicMock):
        url = reverse("plannen:instrumenttype-list")
        data = {
            "instrument_type": InstrumenttypeFactory.build().instrument_type,
            "categorieen_uuids": [str(self.categorie.uuid)],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        mock_add.assert_called_once_with(1)

    @patch.object(
        instrumenttypen_update_counter, "add", wraps=instrumenttypen_update_counter.add
    )
    def test_update_instrumenttype_increments_metric(self, mock_add: MagicMock):
        instrumenttype = InstrumenttypeFactory.create(categorieen=[self.categorie])
        new_type = InstrumenttypeFactory.build().instrument_type
        url = reverse(
            "plannen:instrumenttype-detail", kwargs={"uuid": instrumenttype.uuid}
        )
        data = {
            "instrument_type": new_type,
            "categorieen_uuids": [str(self.categorie.uuid)],
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        mock_add.assert_called_once_with(1)

    @patch.object(
        instrumenttypen_delete_counter, "add", wraps=instrumenttypen_delete_counter.add
    )
    def test_delete_instrumenttype_increments_metric(self, mock_add: MagicMock):
        instrumenttype = InstrumenttypeFactory.create()
        url = reverse(
            "plannen:instrumenttype-detail", kwargs={"uuid": instrumenttype.uuid}
        )
        response = self.client.delete(url)
        self.assertIn(response.status_code, (200, 204))
        mock_add.assert_called_once_with(1)
