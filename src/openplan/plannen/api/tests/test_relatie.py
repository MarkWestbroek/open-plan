from unittest.mock import MagicMock, patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.metrics import (
    relaties_create_counter,
    relaties_delete_counter,
    relaties_update_counter,
)
from openplan.plannen.models.factories.persoon import PersoonFactory
from openplan.plannen.models.factories.relatie import RelatieFactory
from openplan.plannen.models.factories.relatietype import RelatieTypeFactory

from ...models.relatie import Relatie
from .api_testcase import APITestCase


class RelatieAPITests(APITestCase):
    def test_create_relatie(self):
        persoon = PersoonFactory.create()
        gerelateerde_persoon = PersoonFactory.create()
        relatietype = RelatieTypeFactory.create()

        url = reverse("plannen:relatie-list")
        data = {
            "persoon_uuid": str(persoon.uuid),
            "gerelateerde_persoon_uuid": str(gerelateerde_persoon.uuid),
            "relatietype_uuid": str(relatietype.uuid),
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        relatie = Relatie.objects.get(uuid=response.data["uuid"])
        self.assertEqual(relatie.persoon, persoon)
        self.assertEqual(relatie.gerelateerde_persoon, gerelateerde_persoon)
        self.assertEqual(relatie.relatietype, relatietype)

    def test_list_relaties(self):
        RelatieFactory.create_batch(3)

        url = reverse("plannen:relatie-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)

        for rel in data:
            self.assertIn("uuid", rel)
            self.assertIn("persoon", rel)
            self.assertIn("gerelateerdePersoon", rel)
            self.assertIn("relatietype", rel)

    def test_retrieve_relatie(self):
        relatie = RelatieFactory.create()

        url = reverse("plannen:relatie-detail", kwargs={"uuid": relatie.uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(relatie.uuid))
        self.assertEqual(
            response.data["persoon"]["uuid"],
            str(relatie.persoon.uuid),
        )
        self.assertEqual(
            response.data["gerelateerde_persoon"]["uuid"],
            str(relatie.gerelateerde_persoon.uuid),
        )

    def test_update_relatie(self):
        relatie = RelatieFactory.create()
        new_relatietype = RelatieTypeFactory.create()

        url = reverse("plannen:relatie-detail", kwargs={"uuid": relatie.uuid})
        data = {
            "persoon_uuid": str(relatie.persoon.uuid),
            "gerelateerde_persoon_uuid": str(relatie.gerelateerde_persoon.uuid),
            "relatietype_uuid": str(new_relatietype.uuid),
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        relatie.refresh_from_db()
        self.assertEqual(relatie.relatietype, new_relatietype)

    def test_partial_update_relatie(self):
        relatie = RelatieFactory.create()
        new_relatietype = RelatieTypeFactory.create()

        url = reverse("plannen:relatie-detail", kwargs={"uuid": relatie.uuid})
        data = {
            "relatietype_uuid": str(new_relatietype.uuid),
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        relatie.refresh_from_db()
        self.assertEqual(relatie.relatietype, new_relatietype)

    def test_delete_relatie(self):
        relatie = RelatieFactory.create()

        url = reverse("plannen:relatie-detail", kwargs={"uuid": relatie.uuid})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Relatie.objects.filter(uuid=relatie.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen:relatie-list")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_prevent_duplicate_relatie(self):
        persoon = PersoonFactory.create()
        gerelateerde_persoon = PersoonFactory.create()
        relatietype = RelatieTypeFactory.create()

        RelatieFactory.create(
            persoon=persoon,
            gerelateerde_persoon=gerelateerde_persoon,
            relatietype=relatietype,
        )

        url = reverse("plannen:relatie-list")
        data = {
            "persoon_uuid": str(persoon.uuid),
            "gerelateerde_persoon_uuid": str(gerelateerde_persoon.uuid),
            "relatietype_uuid": str(relatietype.uuid),
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_relatie_met_zichzelf_niet_toegestaan(self):
        persoon = PersoonFactory.create()
        relatietype = RelatieTypeFactory.create()

        url = reverse("plannen:relatie-list")
        data = {
            "persoon_uuid": persoon.uuid,
            "gerelateerde_persoon_uuid": persoon.uuid,
            "relatietype_uuid": relatietype.uuid,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invalid_params", response.data)
        self.assertIn(
            {
                "name": "nonFieldErrors",
                "code": "invalid",
                "reason": "Een persoon kan geen relatie met zichzelf hebben.",
            },
            response.data["invalid_params"],
        )

    def test_omgekeerde_relatie_niet_toegestaan(self):
        persoon_a = PersoonFactory.create()
        persoon_b = PersoonFactory.create()
        relatietype = RelatieTypeFactory.create()

        RelatieFactory.create(
            persoon=persoon_a,
            gerelateerde_persoon=persoon_b,
            relatietype=relatietype,
        )

        url = reverse("plannen:relatie-list")
        data = {
            "persoon_uuid": persoon_b.uuid,
            "gerelateerde_persoon_uuid": persoon_a.uuid,
            "relatietype_uuid": relatietype.uuid,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invalid_params", response.data)

        self.assertIn(
            {
                "name": "nonFieldErrors",
                "code": "invalid",
                "reason": "Deze relatie bestaat al in omgekeerde richting.",
            },
            response.data["invalid_params"],
        )

    @patch.object(relaties_create_counter, "add", wraps=relaties_create_counter.add)
    def test_create_relatie_increments_metric(self, mock_add: MagicMock):
        persoon = PersoonFactory.create()
        gerelateerde_persoon = PersoonFactory.create()
        relatietype = RelatieTypeFactory.create()

        url = reverse("plannen:relatie-list")
        data = {
            "persoon_uuid": str(persoon.uuid),
            "gerelateerde_persoon_uuid": str(gerelateerde_persoon.uuid),
            "relatietype_uuid": str(relatietype.uuid),
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        mock_add.assert_called_once_with(1)

    @patch.object(relaties_update_counter, "add", wraps=relaties_update_counter.add)
    def test_update_relatie_increments_metric(self, mock_add: MagicMock):
        relatie = RelatieFactory.create()
        new_relatietype = RelatieTypeFactory.create()

        url = reverse("plannen:relatie-detail", kwargs={"uuid": relatie.uuid})
        data = {
            "persoon_uuid": str(relatie.persoon.uuid),
            "gerelateerde_persoon_uuid": str(relatie.gerelateerde_persoon.uuid),
            "relatietype_uuid": str(new_relatietype.uuid),
        }

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        mock_add.assert_called_once_with(1)

    @patch.object(relaties_delete_counter, "add", wraps=relaties_delete_counter.add)
    def test_delete_relatie_increments_metric(self, mock_add: MagicMock):
        relatie = RelatieFactory.create()

        url = reverse("plannen:relatie-detail", kwargs={"uuid": relatie.uuid})
        response = self.client.delete(url)
        self.assertIn(response.status_code, (200, 204))
        mock_add.assert_called_once_with(1)
