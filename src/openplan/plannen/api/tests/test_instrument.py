import datetime
from unittest.mock import MagicMock, patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.enums.status import PlanStatus, Resultaat
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

    def test_filter_instrumenttype_uuid(self):
        type1 = self.instrumenttype
        type2 = InstrumenttypeFactory.create()

        inst1 = InstrumentFactory.create(instrumenttype=type1)
        InstrumentFactory.create(instrumenttype=type2)

        url = reverse("plannen:instrument-list")
        response = self.client.get(url, {"instrumenttype__uuid": str(type1.uuid)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(inst1.uuid))

    def test_filter_doelen_uuids(self):
        doel1 = self.doel
        doel2 = DoelFactory.create()
        doel3 = DoelFactory.create()

        inst1 = InstrumentFactory.create(doelen=[doel1])
        inst2 = InstrumentFactory.create(doelen=[doel2])
        InstrumentFactory.create(doelen=[doel3])

        url = reverse("plannen:instrument-list")

        with self.subTest("exact"):
            response = self.client.get(url, {"doelen__uuid": str(doel1.uuid)})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertEqual(response.data["results"][0]["uuid"], str(inst1.uuid))

        with self.subTest("in"):
            response = self.client.get(
                url, {"doelen__uuid__in": f"{doel1.uuid},{doel2.uuid}"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 2)
            uuids = [r["uuid"] for r in response.data["results"]]
            self.assertIn(str(inst1.uuid), uuids)
            self.assertIn(str(inst2.uuid), uuids)

    def test_filter_doelen_uuids_duplicates(self):
        doel1 = self.doel
        doel2 = DoelFactory.create()

        InstrumentFactory.create(doelen=[doel1])
        InstrumentFactory.create(doelen=[doel2])

        InstrumentFactory.create(doelen=[doel1, doel2])

        url = reverse("plannen:instrument-list")

        response = self.client.get(
            url, {"doelen__uuid__in": f"{doel1.uuid},{doel2.uuid}"}
        )
        returned_ids = [r["uuid"] for r in response.data["results"]]

        unique_ids = set(returned_ids)

        self.assertEqual(len(unique_ids), 3)

    def test_invalid_uuid_returns_failure(self):
        url = reverse("plannen:instrument-list")

        response = self.client.get(url, {"doelen__uuid__in": "invalid-uuid"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_error = {
            "name": "doelen__uuid__in",
            "code": "invalid",
            "reason": "Voer een geldige UUID in.",
        }

        self.assertIn("invalid_params", response.data)
        self.assertIn(expected_error, response.data["invalid_params"])

    def test_filter_ontwikkelwensen_uuids(self):
        wens1 = self.ontwikkelwens
        wens2 = OntwikkelwensFactory.create()
        wens3 = OntwikkelwensFactory.create()

        inst1 = InstrumentFactory.create(ontwikkelwensen=[wens1])
        inst2 = InstrumentFactory.create(ontwikkelwensen=[wens2])
        InstrumentFactory.create(ontwikkelwensen=[wens3])

        url = reverse("plannen:instrument-list")

        with self.subTest("exact"):
            response = self.client.get(url, {"ontwikkelwensen__uuid": str(wens1.uuid)})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertEqual(response.data["results"][0]["uuid"], str(inst1.uuid))

        with self.subTest("in"):
            response = self.client.get(
                url, {"ontwikkelwensen__uuid__in": f"{wens1.uuid},{wens2.uuid}"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 2)
            uuids = [r["uuid"] for r in response.data["results"]]
            self.assertIn(str(inst1.uuid), uuids)
            self.assertIn(str(inst2.uuid), uuids)

    def test_filter_instrument_categorieen_uuids(self):
        cat1 = self.categorie
        cat2 = InstrumentCategorieFactory.create()
        cat3 = InstrumentCategorieFactory.create()

        inst1 = InstrumentFactory.create(instrument_categorieen=[cat1])
        inst2 = InstrumentFactory.create(instrument_categorieen=[cat2])
        InstrumentFactory.create(instrument_categorieen=[cat3])

        url = reverse("plannen:instrument-list")

        with self.subTest("exact"):
            response = self.client.get(
                url, {"instrument_categorieen__uuid": str(cat1.uuid)}
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertEqual(response.data["results"][0]["uuid"], str(inst1.uuid))

        with self.subTest("in"):
            response = self.client.get(
                url,
                {
                    "instrument_categorieen__uuid__in": f"{cat1.uuid},{cat2.uuid}",
                },
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 2)

            uuids = [r["uuid"] for r in response.data["results"]]
            self.assertIn(str(inst1.uuid), uuids)
            self.assertIn(str(inst2.uuid), uuids)

    def test_filter_product(self):
        inst1 = InstrumentFactory.create(product="urn:example:product:1")
        InstrumentFactory.create(product="urn:example:product:2")

        url = reverse("plannen:instrument-list")
        response = self.client.get(url, {"product": "urn:example:product:1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(inst1.uuid))

    def test_filter_zaak(self):
        inst1 = InstrumentFactory.create(zaak="urn:example:zaak:1")
        InstrumentFactory.create(zaak="urn:example:zaak:2")

        url = reverse("plannen:instrument-list")
        response = self.client.get(url, {"zaak": "urn:example:zaak:1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(inst1.uuid))

    def test_filter_status(self):
        InstrumentFactory.create(status=PlanStatus.ACTIEF)
        InstrumentFactory.create(status=PlanStatus.AFGEROND)

        url = reverse("plannen:instrument-list")
        response = self.client.get(url, {"status": "actief"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["status"], "actief")

    def test_filter_titel(self):
        InstrumentFactory.create(titel="Alpha Instrument")
        InstrumentFactory.create(titel="Beta Instrument")

        url = reverse("plannen:instrument-list")

        with self.subTest("exact"):
            response = self.client.get(url, {"titel": "Alpha Instrument"})
            self.assertEqual(response.data["count"], 1)

        with self.subTest("icontains"):
            response = self.client.get(url, {"titel__icontains": "beta"})
            self.assertEqual(response.data["count"], 1)

    def test_filter_resultaat(self):
        InstrumentFactory.create(resultaat=Resultaat.BEHAALD)
        InstrumentFactory.create(resultaat=Resultaat.GEFAALD)

        url = reverse("plannen:instrument-list")
        response = self.client.get(url, {"resultaat": "behaald"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["resultaat"], "behaald")

    def test_filter_startdatum(self):
        InstrumentFactory.create(startdatum="2024-06-07T00:00:00Z")
        InstrumentFactory.create(startdatum="2025-06-07T00:00:00Z")

        url = reverse("plannen:instrument-list")

        with self.subTest("exact"):
            response = self.client.get(url, {"startdatum": "2024-06-07T00:00:00Z"})
            self.assertEqual(response.data["count"], 1)

        with self.subTest("lte"):
            response = self.client.get(url, {"startdatum__lte": "2024-07-07T00:00:00Z"})
            self.assertEqual(response.data["count"], 1)

        with self.subTest("gte"):
            response = self.client.get(url, {"startdatum__gte": "2025-04-07T00:00:00Z"})
            self.assertEqual(response.data["count"], 1)

    def test_filter_einddatum(self):
        InstrumentFactory.create(einddatum="2024-06-07T00:00:00Z")
        InstrumentFactory.create(einddatum="2025-06-07T00:00:00Z")

        url = reverse("plannen:instrument-list")

        with self.subTest("exact"):
            response = self.client.get(url, {"einddatum": "2024-06-07T00:00:00Z"})
            self.assertEqual(response.data["count"], 1)

        with self.subTest("lte"):
            response = self.client.get(url, {"einddatum__lte": "2024-07-07T00:00:00Z"})
            self.assertEqual(response.data["count"], 1)

        with self.subTest("gte"):
            response = self.client.get(url, {"einddatum__gte": "2025-04-07T00:00:00Z"})
            self.assertEqual(response.data["count"], 1)

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
