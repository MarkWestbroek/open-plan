from unittest.mock import MagicMock, patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.metrics import (
    instrumenten_create_counter,
    instrumenten_delete_counter,
    instrumenten_update_counter,
)
from openplan.plannen.models.factories.doel import DoelFactory
from openplan.plannen.models.factories.instrument import InstrumentFactory
from openplan.plannen.models.factories.instrumenttype import InstrumenttypeFactory

from ...models.instrument import Instrument
from .api_testcase import APITestCase


class InstrumentAPITests(APITestCase):
    def test_create_instrument(self):
        doel = DoelFactory.create()
        instrumenttype = InstrumenttypeFactory.create()

        url = reverse("plannen:instrument-list")
        data = {
            "doel_uuid": doel.uuid,
            "instrumenttype_uuid": instrumenttype.uuid,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        instrument = Instrument.objects.get(uuid=response.data["uuid"])
        self.assertEqual(instrument.doel, doel)
        self.assertEqual(instrument.instrumenttype, instrumenttype)

    def test_list_instrumenten(self):
        InstrumentFactory.create_batch(3)

        url = reverse("plannen:instrument-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)
        for inst in data:
            self.assertIn("uuid", inst)
            self.assertIn("doel", inst)
            self.assertIn("instrumenttype", inst)

    def test_retrieve_instrument(self):
        instrument = InstrumentFactory.create()
        url = reverse("plannen:instrument-detail", kwargs={"uuid": instrument.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(instrument.uuid))
        self.assertEqual(response.data["doel"]["uuid"], str(instrument.doel.uuid))
        self.assertEqual(
            response.data["instrumenttype"]["uuid"], str(instrument.instrumenttype.uuid)
        )

    def test_update_instrument(self):
        instrument = InstrumentFactory.create()
        new_doel = DoelFactory.create()
        new_instrumenttype = InstrumenttypeFactory.create()

        url = reverse("plannen:instrument-detail", kwargs={"uuid": instrument.uuid})
        data = {
            "doel_uuid": new_doel.uuid,
            "instrumenttype_uuid": new_instrumenttype.uuid,
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        instrument.refresh_from_db()
        self.assertEqual(instrument.doel, new_doel)
        self.assertEqual(instrument.instrumenttype, new_instrumenttype)

    def test_partial_update_instrument(self):
        instrument = InstrumentFactory.create()
        new_doel = DoelFactory.create()

        url = reverse("plannen:instrument-detail", kwargs={"uuid": instrument.uuid})
        data = {"doel_uuid": new_doel.uuid}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        instrument.refresh_from_db()
        self.assertEqual(instrument.doel, new_doel)

    def test_delete_instrument(self):
        instrument = InstrumentFactory.create()
        url = reverse("plannen:instrument-detail", kwargs={"uuid": instrument.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Instrument.objects.filter(uuid=instrument.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen:instrument-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch.object(
        instrumenten_create_counter, "add", wraps=instrumenten_create_counter.add
    )
    def test_create_instrument_increments_metric(self, mock_add: MagicMock):
        doel = DoelFactory.create()
        instrumenttype = InstrumenttypeFactory.create()

        url = reverse("plannen:instrument-list")
        data = {
            "doel_uuid": doel.uuid,
            "instrumenttype_uuid": instrumenttype.uuid,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        mock_add.assert_called_once_with(1)

    @patch.object(
        instrumenten_update_counter, "add", wraps=instrumenten_update_counter.add
    )
    def test_update_instrument_increments_metric(self, mock_add: MagicMock):
        instrument = InstrumentFactory.create()
        new_doel = DoelFactory.create()
        new_instrumenttype = InstrumenttypeFactory.create()

        url = reverse("plannen:instrument-detail", kwargs={"uuid": instrument.uuid})
        data = {
            "doel_uuid": new_doel.uuid,
            "instrumenttype_uuid": new_instrumenttype.uuid,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        mock_add.assert_called_once_with(1)

    @patch.object(
        instrumenten_delete_counter, "add", wraps=instrumenten_delete_counter.add
    )
    def test_delete_instrument_increments_metric(self, mock_add: MagicMock):
        instrument = InstrumentFactory.create()
        url = reverse("plannen:instrument-detail", kwargs={"uuid": instrument.uuid})
        response = self.client.delete(url)
        self.assertIn(response.status_code, (200, 204))
        mock_add.assert_called_once_with(1)
