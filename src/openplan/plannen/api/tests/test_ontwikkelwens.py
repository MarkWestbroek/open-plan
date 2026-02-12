import datetime

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.enums.status import PlanStatus, Resultaat
from openplan.plannen.models.factories.doel import DoelFactory
from openplan.plannen.models.factories.doelcategorie import DoelCategorieFactory
from openplan.plannen.models.factories.ontwikkelwens import OntwikkelwensFactory

from ...models.ontwikkelwens import Ontwikkelwens
from .api_testcase import APITestCase


class OntwikkelwensAPITests(APITestCase):
    def setUp(self):
        super().setUp()
        self.doel = DoelFactory.create()
        self.doel_categorie = DoelCategorieFactory.create()

        self.data = {
            "titel": "Test Ontwikkelwens",
            "startdatum": datetime.date.today().isoformat(),
            "doel_uuid": str(self.doel.uuid),
            "doel_categorieen_uuids": [str(self.doel_categorie.uuid)],
        }

    def test_create_ontwikkelwens(self):
        url = reverse("plannen:ontwikkelwens-list")
        response = self.client.post(url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ow = Ontwikkelwens.objects.get(uuid=response.data["uuid"])
        self.assertEqual(ow.doel, self.doel)
        self.assertIn(self.doel_categorie, ow.doel_categorieen.all())

    def test_list_ontwikkelwensen(self):
        url = reverse("plannen:ontwikkelwens-list")
        OntwikkelwensFactory.create_batch(2, doel=self.doel)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 2)

        for ow in data:
            self.assertIn("uuid", ow)
            self.assertIn("doel", ow)

    def test_retrieve_ontwikkelwens(self):
        ow = OntwikkelwensFactory.create(doel=self.doel)
        ow.doel_categorieen.add(self.doel_categorie)

        url = reverse("plannen:ontwikkelwens-detail", kwargs={"uuid": ow.uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(ow.uuid))
        self.assertEqual(response.data["doel"]["uuid"], str(self.doel.uuid))

    def test_update_ontwikkelwens(self):
        ow = OntwikkelwensFactory.create(doel=self.doel)
        new_doel = DoelFactory.create()

        url = reverse("plannen:ontwikkelwens-detail", kwargs={"uuid": ow.uuid})
        data = {
            "titel": "Updated Ontwikkelwens",
            "startdatum": datetime.date.today().isoformat(),
            "doel_uuid": str(new_doel.uuid),
            "doel_categorieen_uuids": [str(self.doel_categorie.uuid)],
        }

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ow.refresh_from_db()
        self.assertEqual(ow.doel, new_doel)

    def test_partial_update_ontwikkelwens(self):
        ow = OntwikkelwensFactory.create(doel=self.doel)
        new_doel = DoelFactory.create()

        url = reverse("plannen:ontwikkelwens-detail", kwargs={"uuid": ow.uuid})
        response = self.client.patch(
            url, {"doel_uuid": str(new_doel.uuid)}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ow.refresh_from_db()
        self.assertEqual(ow.doel, new_doel)

    def test_delete_ontwikkelwens(self):
        ow = OntwikkelwensFactory.create(doel=self.doel)

        url = reverse("plannen:ontwikkelwens-detail", kwargs={"uuid": ow.uuid})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ontwikkelwens.objects.filter(uuid=ow.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen:ontwikkelwens-list")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_doel_uuid(self):
        ow1 = OntwikkelwensFactory.create(doel=self.doel)
        OntwikkelwensFactory.create(doel=DoelFactory.create())

        url = reverse("plannen:ontwikkelwens-list")
        response = self.client.get(url, {"doel_uuid": str(self.doel.uuid)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(ow1.uuid))

    def test_filter_doel_categorieen_uuids(self):
        ow1 = OntwikkelwensFactory.create(doel=self.doel)
        ow1.doel_categorieen.add(self.doel_categorie)

        other = OntwikkelwensFactory.create(doel=self.doel)
        other.doel_categorieen.add(DoelCategorieFactory.create())

        url = reverse("plannen:ontwikkelwens-list")
        response = self.client.get(
            url,
            {"doel_categorieen_uuids": str(self.doel_categorie.uuid)},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(ow1.uuid))

    def test_filter_status(self):
        OntwikkelwensFactory.create(status=PlanStatus.AFGEROND)
        OntwikkelwensFactory.create(status=PlanStatus.ACTIEF)

        url = reverse("plannen:ontwikkelwens-list")
        response = self.client.get(url, {"status": "afgerond"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_filter_titel(self):
        OntwikkelwensFactory.create(titel="Nieuwe Feature")
        OntwikkelwensFactory.create(titel="Bugfix")

        url = reverse("plannen:ontwikkelwens-list")

        with self.subTest("exact"):
            response = self.client.get(url, {"titel": "Nieuwe Feature"})
            self.assertEqual(response.data["count"], 1)

        with self.subTest("icontains"):
            response = self.client.get(url, {"titel__icontains": "Feature"})
            self.assertEqual(response.data["count"], 1)

    def test_filter_resultaat(self):
        OntwikkelwensFactory.create(resultaat=Resultaat.BEHAALD)
        OntwikkelwensFactory.create(resultaat=Resultaat.GEFAALD)

        url = reverse("plannen:ontwikkelwens-list")

        response = self.client.get(url, {"resultaat": "behaald"})
        self.assertEqual(response.data["count"], 1)

    def test_filter_startdatum(self):
        OntwikkelwensFactory.create(
            startdatum=timezone.make_aware(datetime.datetime(2026, 1, 1))
        )
        OntwikkelwensFactory.create(
            startdatum=timezone.make_aware(datetime.datetime(2026, 2, 1))
        )

        url = reverse("plannen:ontwikkelwens-list")

        with self.subTest("exact"):
            response = self.client.get(url, {"startdatum": "2026-01-01"})
            self.assertEqual(response.data["count"], 1)

        with self.subTest("lte"):
            response = self.client.get(url, {"startdatum__lte": "2026-01-15"})
            self.assertEqual(response.data["count"], 1)

        with self.subTest("gte"):
            response = self.client.get(url, {"startdatum__gte": "2026-02-01"})
            self.assertEqual(response.data["count"], 1)

    def test_filter_einddatum(self):
        OntwikkelwensFactory.create(
            einddatum=timezone.make_aware(datetime.datetime(2026, 1, 15))
        )
        OntwikkelwensFactory.create(
            einddatum=timezone.make_aware(datetime.datetime(2026, 2, 15))
        )

        url = reverse("plannen:ontwikkelwens-list")

        with self.subTest("exact"):
            response = self.client.get(url, {"einddatum": "2026-01-15"})
            self.assertEqual(response.data["count"], 1)

        with self.subTest("lte"):
            response = self.client.get(url, {"einddatum__lte": "2026-01-31"})
            self.assertEqual(response.data["count"], 1)

        with self.subTest("gte"):
            response = self.client.get(url, {"einddatum__gte": "2026-02-01"})
            self.assertEqual(response.data["count"], 1)
