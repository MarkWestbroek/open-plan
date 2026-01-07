from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.models.factories.persoon import PersoonFactory

from ...models.persoon import Persoon
from .api_testcase import APITestCase


class PersoonAPITests(APITestCase):
    def test_create_persoon(self):
        url = reverse("plannen:persoon-list")
        data = {
            "persoonsprofiel_url": "https://example.com/profiel",
            "open_klant_url": "https://example.com/klant",
            "bsn": "111222333",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        persoon = Persoon.objects.get(uuid=response.data["uuid"])
        self.assertEqual(persoon.persoonsprofiel_url, data["persoonsprofiel_url"])
        self.assertEqual(persoon.open_klant_url, data["open_klant_url"])
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
            self.assertIn("persoonsprofielUrl", p)
            self.assertIn("openKlantUrl", p)
            self.assertIn("bsn", p)

    def test_retrieve_persoon(self):
        persoon = PersoonFactory.create()
        url = reverse("plannen:persoon-detail", kwargs={"uuid": persoon.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(persoon.uuid))
        self.assertEqual(
            response.data["persoonsprofiel_url"], persoon.persoonsprofiel_url
        )
        self.assertEqual(response.data["open_klant_url"], persoon.open_klant_url)
        self.assertEqual(response.data["bsn"], persoon.bsn)

    def test_update_persoon(self):
        persoon = PersoonFactory.create()
        new_data = {
            "persoonsprofiel_url": "https://example.com/newprofiel",
            "open_klant_url": "https://example.com/newklant",
            "bsn": "111222333",
        }
        url = reverse("plannen:persoon-detail", kwargs={"uuid": persoon.uuid})
        response = self.client.put(url, new_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        persoon.refresh_from_db()
        self.assertEqual(persoon.persoonsprofiel_url, new_data["persoonsprofiel_url"])
        self.assertEqual(persoon.open_klant_url, new_data["open_klant_url"])
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
