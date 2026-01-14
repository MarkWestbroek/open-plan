from unittest.mock import MagicMock, patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.metrics import (
    doelcategorieen_create_counter,
    doelcategorieen_delete_counter,
    doelcategorieen_update_counter,
)
from openplan.plannen.models.factories.doelcategorie import DoelCategorieFactory

from ...models.doelcategorie import DoelCategorie
from .api_testcase import APITestCase


class DoelCategorieAPITests(APITestCase):
    def test_create_doelcategorie(self):
        url = reverse("plannen:doelcategorie-list")
        data = {"naam": DoelCategorieFactory.build().naam}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        categorie = DoelCategorie.objects.get(uuid=response.data["uuid"])
        self.assertEqual(categorie.naam, data["naam"])

    def test_list_doelcategorieen(self):
        DoelCategorieFactory.create_batch(3)

        url = reverse("plannen:doelcategorie-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)
        for dc in data:
            self.assertIn("uuid", dc)
            self.assertIn("naam", dc)

    def test_retrieve_doelcategorie(self):
        categorie = DoelCategorieFactory.create()
        url = reverse("plannen:doelcategorie-detail", kwargs={"uuid": categorie.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(categorie.uuid))
        self.assertEqual(response.data["naam"], categorie.naam)

    def test_update_doelcategorie(self):
        categorie = DoelCategorieFactory.create()
        new_naam = DoelCategorieFactory.build().naam

        url = reverse("plannen:doelcategorie-detail", kwargs={"uuid": categorie.uuid})
        data = {"naam": new_naam}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categorie.refresh_from_db()
        self.assertEqual(categorie.naam, new_naam)

    def test_partial_update_doelcategorie(self):
        categorie = DoelCategorieFactory.create()
        new_naam = DoelCategorieFactory.build().naam

        url = reverse("plannen:doelcategorie-detail", kwargs={"uuid": categorie.uuid})
        data = {"naam": new_naam}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categorie.refresh_from_db()
        self.assertEqual(categorie.naam, new_naam)

    def test_delete_doelcategorie(self):
        categorie = DoelCategorieFactory.create()
        url = reverse("plannen:doelcategorie-detail", kwargs={"uuid": categorie.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DoelCategorie.objects.filter(uuid=categorie.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen:doelcategorie-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_doelcategorie_by_naam(self):
        categorie_match = DoelCategorieFactory.create(naam="Strategie")
        DoelCategorieFactory.create(naam="Marketing")
        DoelCategorieFactory.create(naam="Productie")

        url = reverse("plannen:doelcategorie-list")
        response = self.client.get(url, {"naam": "Strategie"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["uuid"], str(categorie_match.uuid))
        self.assertEqual(data["results"][0]["naam"], "Strategie")

    @patch.object(
        doelcategorieen_create_counter, "add", wraps=doelcategorieen_create_counter.add
    )
    def test_create_doelcategorie_increments_metric(self, mock_add: MagicMock):
        url = reverse("plannen:doelcategorie-list")
        data = {"naam": DoelCategorieFactory.build().naam}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        mock_add.assert_called_once_with(1)

    @patch.object(
        doelcategorieen_update_counter, "add", wraps=doelcategorieen_update_counter.add
    )
    def test_update_doelcategorie_increments_metric(self, mock_add: MagicMock):
        categorie = DoelCategorieFactory.create()
        new_naam = DoelCategorieFactory.build().naam

        url = reverse("plannen:doelcategorie-detail", kwargs={"uuid": categorie.uuid})
        data = {"naam": new_naam}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        mock_add.assert_called_once_with(1)

    @patch.object(
        doelcategorieen_delete_counter, "add", wraps=doelcategorieen_delete_counter.add
    )
    def test_delete_doelcategorie_increments_metric(self, mock_add: MagicMock):
        categorie = DoelCategorieFactory.create()
        url = reverse("plannen:doelcategorie-detail", kwargs={"uuid": categorie.uuid})
        response = self.client.delete(url)
        self.assertIn(response.status_code, (200, 204))
        mock_add.assert_called_once_with(1)
