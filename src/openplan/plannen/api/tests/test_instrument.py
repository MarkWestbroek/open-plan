import datetime
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
from openplan.plannen.models.factories.instrumentcategorie import (
    InstrumentCategorieFactory,
)
from openplan.plannen.models.factories.instrumenttype import InstrumenttypeFactory
from openplan.plannen.models.factories.ontwikkelwens import OntwikkelwensFactory

from ...models.instrument import Instrument
from .api_testcase import APITestCase


class InstrumentAPITests(APITestCase):
    def setUp(self):
        super().setUp()
        self.doel = DoelFactory.create()
        self.instrumenttype = InstrumenttypeFactory.create()
        self.categorie = InstrumentCategorieFactory.create()
        self.ontwikkelwens = OntwikkelwensFactory.create()

        self.data = {
            "titel": "Test Instrument",
            "startdatum": datetime.date.today().isoformat(),
            "doelen_uuids": [str(self.doel.uuid)],
            "ontwikkelwensen_uuids": [str(self.ontwikkelwens.uuid)],
            "instrumenttype_uuid": str(self.instrumenttype.uuid),
            "instrument_categorieen_uuids": [str(self.categorie.uuid)],
        }

    def test_create_instrument(self):
        url = reverse("plannen:instrument-list")
        response = self.client.post(url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        instrument = Instrument.objects.get(uuid=response.data["uuid"])
        self.assertIn(self.doel, instrument.doelen.all())
        self.assertEqual(instrument.instrumenttype, self.instrumenttype)

    def test_list_instrumenten(self):
        url = reverse("plannen:instrument-list")
        InstrumentFactory.create_batch(2, doelen=[self.doel])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 2)
        for inst in data:
            self.assertIn("uuid", inst)
            self.assertIn("doelen", inst)
            self.assertIn("instrumenttype", inst)

    def test_retrieve_instrument(self):
        instrument = InstrumentFactory.create(doelen=[self.doel])
        url = reverse("plannen:instrument-detail", kwargs={"uuid": instrument.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(instrument.uuid))
        self.assertIn(str(self.doel.uuid), [d["uuid"] for d in response.data["doelen"]])
        self.assertEqual(
            response.data["instrumenttype"]["uuid"], str(instrument.instrumenttype.uuid)
        )

    def test_update_instrument(self):
        instrument = InstrumentFactory.create(doelen=[self.doel])
        new_doel = DoelFactory.create(doeltype=self.doel.doeltype)
        new_instrumenttype = InstrumenttypeFactory.create()

        url = reverse("plannen:instrument-detail", kwargs={"uuid": instrument.uuid})
        data = {
            "titel": "Test update Instrument",
            "startdatum": datetime.date.today().isoformat(),
            "doelen_uuids": [str(new_doel.uuid)],
            "ontwikkelwensen_uuids": [str(self.ontwikkelwens.uuid)],
            "instrumenttype_uuid": new_instrumenttype.uuid,
            "instrument_categorieen_uuids": [str(self.categorie.uuid)],
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        instrument.refresh_from_db()
        doelen_uuids = list(instrument.doelen.values_list("uuid", flat=True))
        self.assertIn(new_doel.uuid, doelen_uuids)
        self.assertEqual(len(doelen_uuids), 1)

        self.assertEqual(instrument.instrumenttype, new_instrumenttype)

    def test_partial_update_instrument(self):
        instrument = InstrumentFactory.create(doelen=[self.doel])
        new_doel = DoelFactory.create(doeltype=self.doel.doeltype)

        url = reverse("plannen:instrument-detail", kwargs={"uuid": instrument.uuid})
        data = {"doelen_uuids": [str(new_doel.uuid)]}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        instrument.refresh_from_db()
        doelen_uuids = list(instrument.doelen.values_list("uuid", flat=True))

        self.assertIn(new_doel.uuid, doelen_uuids)
        self.assertEqual(len(doelen_uuids), 1)

    def test_delete_instrument(self):
        instrument = InstrumentFactory.create(doelen=[self.doel])
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
        url = reverse("plannen:instrument-list")
        response = self.client.post(url, self.data, format="json")

        self.assertEqual(response.status_code, 201)
        mock_add.assert_called_once_with(1)

    @patch.object(
        instrumenten_update_counter, "add", wraps=instrumenten_update_counter.add
    )
    def test_update_instrument_increments_metric(self, mock_add: MagicMock):
        instrument = InstrumentFactory.create(doelen=[self.doel])
        new_doel = DoelFactory.create(doeltype=self.doel.doeltype)
        new_instrumenttype = InstrumenttypeFactory.create()

        url = reverse("plannen:instrument-detail", kwargs={"uuid": instrument.uuid})
        data = {
            "titel": "Test update Instrument",
            "startdatum": datetime.date.today().isoformat(),
            "doelen_uuids": [str(new_doel.uuid)],
            "ontwikkelwensen_uuids": [str(self.ontwikkelwens.uuid)],
            "instrumenttype_uuid": new_instrumenttype.uuid,
            "instrument_categorieen_uuids": [str(self.categorie.uuid)],
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        mock_add.assert_called_once_with(1)

    @patch.object(
        instrumenten_delete_counter, "add", wraps=instrumenten_delete_counter.add
    )
    def test_delete_instrument_increments_metric(self, mock_add: MagicMock):
        instrument = InstrumentFactory.create(doelen=[self.doel])
        url = reverse("plannen:instrument-detail", kwargs={"uuid": instrument.uuid})
        response = self.client.delete(url)
        self.assertIn(response.status_code, (200, 204))
        mock_add.assert_called_once_with(1)
