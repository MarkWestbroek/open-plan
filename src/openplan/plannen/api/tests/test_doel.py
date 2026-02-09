from datetime import date
from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.metrics import (
    doelen_create_counter,
    doelen_delete_counter,
    doelen_update_counter,
)
from openplan.plannen.models.factories.doel import DoelFactory
from openplan.plannen.models.factories.doeltype import DoelTypeFactory
from openplan.plannen.models.factories.persoon import PersoonFactory
from openplan.plannen.models.factories.plan import PlanFactory

from ...models.doel import Doel
from .api_testcase import APITestCase


class DoelAPITests(APITestCase):
    def setUp(self):
        super().setUp()
        self.hoofddoel_type = DoelTypeFactory.create(doel_type="hoofddoel")
        self.subdoel_type = DoelTypeFactory.create(doel_type="subdoel")

        self.plan = PlanFactory.create()
        self.persoon = PersoonFactory.create()

        self.data = {
            "doeltypeUuid": str(self.hoofddoel_type.uuid),
            "plannenUuids": [str(self.plan.uuid)],
            "persoonUuid": str(self.persoon.uuid),
            "titel": "Test Doel",
            "startdatum": str(date.today()),
            "beschrijving": "Beschrijving test",
        }

    def test_create_doel(self):
        url = reverse("plannen:doel-list")
        response = self.client.post(url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        doel = Doel.objects.get(uuid=response.data["uuid"])
        self.assertEqual(doel.doeltype.uuid, self.hoofddoel_type.uuid)

    def test_list_doelens(self):
        doeltype = self.hoofddoel_type
        DoelFactory.create_batch(
            3, doeltype=doeltype, plannen=[self.plan], persoon=self.persoon
        )

        url = reverse("plannen:doel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)

        for doel_data in data:
            self.assertIn("uuid", doel_data)
            self.assertIn("doeltype", doel_data)

    def test_retrieve_doel(self):
        doeltype = self.hoofddoel_type
        doel = DoelFactory.create(doeltype=doeltype)

        url = reverse("plannen:doel-detail", kwargs={"uuid": doel.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(doel.uuid))
        self.assertEqual(response.data["doeltype"]["doel_type"], str(doel.doeltype))

    def test_update_doel(self):
        doeltype = self.hoofddoel_type
        doel = DoelFactory.create(doeltype=doeltype)
        new_doeltype = self.subdoel_type
        new_plan = PlanFactory.create()
        url = reverse("plannen:doel-detail", kwargs={"uuid": doel.uuid})
        data = {
            "doeltypeUuid": str(new_doeltype.uuid),
            "plannenUuids": [str(new_plan.uuid)],
            "persoonUuid": str(doel.persoon.uuid),
            "titel": "Test update Doel",
            "startdatum": str(date.today()),
            "beschrijving": "Beschrijving update test",
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        doel.refresh_from_db()
        self.assertEqual(doel.doeltype.uuid, new_doeltype.uuid)

    def test_partial_update_doel(self):
        doeltype = self.hoofddoel_type
        doel = DoelFactory.create(doeltype=doeltype)
        new_doeltype = self.subdoel_type

        url = reverse("plannen:doel-detail", kwargs={"uuid": doel.uuid})
        data = {"doeltypeUuid": str(new_doeltype.uuid)}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        doel.refresh_from_db()
        self.assertEqual(doel.doeltype.uuid, new_doeltype.uuid)

    def test_delete_doel(self):
        doeltype = self.hoofddoel_type
        doel = DoelFactory.create(doeltype=doeltype)

        url = reverse("plannen:doel-detail", kwargs={"uuid": doel.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doel.objects.filter(uuid=doel.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen:doel-list")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_doeltype_uuid(self):
        type1 = self.hoofddoel_type
        type2 = self.subdoel_type

        doel1 = DoelFactory(doeltype=type1)
        DoelFactory(doeltype=type2)

        url = reverse("plannen:doel-list")
        response = self.client.get(url, {"doeltype_uuid": str(type1.uuid)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(doel1.uuid))

    def test_list_children_under_parent(self):
        parent = DoelFactory(
            doeltype=self.hoofddoel_type, plannen=[self.plan], persoon=self.persoon
        )
        child1 = DoelFactory(
            hoofd_doel=parent,
            doeltype=self.subdoel_type,
            plannen=[self.plan],
            persoon=self.persoon,
        )
        child2 = DoelFactory(
            hoofd_doel=parent,
            doeltype=self.subdoel_type,
            plannen=[self.plan],
            persoon=self.persoon,
        )
        DoelFactory(
            doeltype=self.hoofddoel_type, plannen=[self.plan], persoon=self.persoon
        )

        url = reverse("plannen:doel-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        children = [
            org
            for org in response.data["results"]
            if org.get("hoofd_doel") == str(parent.uuid)
        ]
        self.assertIn(str(child1.uuid), [c["uuid"] for c in children])
        self.assertIn(str(child2.uuid), [c["uuid"] for c in children])

    def test_parent_field_in_detail(self):
        parent = DoelFactory(doeltype=self.hoofddoel_type)
        child = DoelFactory(hoofd_doel=parent, doeltype=self.subdoel_type)

        url = reverse(
            "plannen:doel-detail",
            kwargs={"uuid": child.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["hoofd_doel"], str(parent.uuid))

    def test_multiple_independent_trees(self):
        root1 = DoelFactory(
            doeltype=self.hoofddoel_type, plannen=[self.plan], persoon=self.persoon
        )
        root2 = DoelFactory(
            doeltype=self.hoofddoel_type, plannen=[self.plan], persoon=self.persoon
        )

        child1a = DoelFactory(
            hoofd_doel=root1,
            doeltype=self.subdoel_type,
            plannen=[self.plan],
            persoon=self.persoon,
        )
        child1b = DoelFactory(
            hoofd_doel=root1,
            doeltype=self.subdoel_type,
            plannen=[self.plan],
            persoon=self.persoon,
        )
        child2a = DoelFactory(
            hoofd_doel=root2,
            doeltype=self.subdoel_type,
            plannen=[self.plan],
            persoon=self.persoon,
        )

        url = reverse("plannen:doel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.data["results"]

        roots = [org for org in data if org.get("hoofd_doel") is None]
        self.assertIn(str(root1.uuid), [r["uuid"] for r in roots])
        self.assertIn(str(root2.uuid), [r["uuid"] for r in roots])
        self.assertEqual(len(roots), 2)

        children_root1 = [
            org["uuid"] for org in data if org.get("hoofd_doel") == str(root1.uuid)
        ]
        children_root2 = [
            org["uuid"] for org in data if org.get("hoofd_doel") == str(root2.uuid)
        ]

        self.assertIn(str(child1a.uuid), children_root1)
        self.assertIn(str(child1b.uuid), children_root1)
        self.assertIn(str(child2a.uuid), children_root2)

    def test_prevent_cycle_in_parent(self):
        parent = DoelFactory(doeltype=self.hoofddoel_type)
        child = DoelFactory(hoofd_doel=parent, doeltype=self.subdoel_type)

        parent.hoofd_doel = child
        with self.assertRaises(ValidationError) as val:
            parent.clean()
        self.assertIn(
            "hoofd_doel",
            val.exception.message_dict,
        )
        self.assertIn(
            "Een hoofd doel kan geen kind als bovenliggende doel hebben.",
            val.exception.message_dict["hoofd_doel"][0],
        )

    def test_prevent_self_parenting(self):
        org = DoelFactory(doeltype=self.hoofddoel_type)
        org.hoofd_doel = org
        with self.assertRaises(ValidationError) as val:
            org.clean()
        self.assertIn(
            "hoofd_doel",
            val.exception.message_dict,
        )
        self.assertIn(
            "Een doel kan niet naar zichzelf verwijzen.",
            val.exception.message_dict["hoofd_doel"][0],
        )

    def test_create_doel_fails_with_multiple_persoon_errors(self):
        persoon = PersoonFactory.create(persoonsprofiel="", klant="", bsn="")

        url = reverse("plannen:doel-list")
        data = {
            "doeltypeUuid": str(self.hoofddoel_type.uuid),
            "plannenUuids": [str(self.plan.uuid)],
            "persoonUuid": str(persoon.uuid),
            "titel": "Test Doel",
            "startdatum": str(date.today()),
            "beschrijving": "Beschrijving test",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        persoon_errors = [
            p["reason"]
            for p in response.data.get("invalid_params", [])
            if p["name"] == "persoon"
        ]

        self.assertEqual(
            persoon_errors,
            [
                "Primair persoon moet een persoonsprofiel URL hebben.",
                "Primair persoon moet een Open Klant koppeling hebben.",
                "Primair persoon moet een BRP-koppeling (BSN) hebben.",
            ],
        )

    @patch.object(doelen_create_counter, "add", wraps=doelen_create_counter.add)
    def test_create_doel_increments_metric(self, mock_add: MagicMock):
        url = reverse("plannen:doel-list")

        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, 201)
        mock_add.assert_called_once_with(1)

    @patch.object(doelen_update_counter, "add", wraps=doelen_update_counter.add)
    def test_update_doel_increments_metric(self, mock_add: MagicMock):
        doel = DoelFactory.create(
            doeltype=self.hoofddoel_type, plannen=[self.plan], persoon=self.persoon
        )
        new_doeltype = self.subdoel_type
        new_plan = PlanFactory.create()
        url = reverse("plannen:doel-detail", kwargs={"uuid": doel.uuid})
        data = {
            "doeltypeUuid": str(new_doeltype.uuid),
            "plannenUuids": [str(new_plan.uuid)],
            "persoonUuid": str(doel.persoon.uuid),
            "titel": "Test update Doel",
            "startdatum": str(date.today()),
            "beschrijving": "Beschrijving update test",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        mock_add.assert_called_once_with(1)

    @patch.object(doelen_delete_counter, "add", wraps=doelen_delete_counter.add)
    def test_delete_doel_increments_metric(self, mock_add: MagicMock):
        doel = DoelFactory.create(
            doeltype=self.hoofddoel_type, plannen=[self.plan], persoon=self.persoon
        )
        url = reverse("plannen:doel-detail", kwargs={"uuid": doel.uuid})
        response = self.client.delete(url)
        self.assertIn(response.status_code, (200, 204))
        mock_add.assert_called_once_with(1)
