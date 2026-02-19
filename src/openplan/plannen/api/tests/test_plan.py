from datetime import date, datetime
from unittest.mock import MagicMock, patch

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient
from vng_api_common.tests import get_validation_errors

from openplan.plannen.enums.status import PlanStatus
from openplan.plannen.metrics import (
    plannen_create_counter,
    plannen_delete_counter,
    plannen_update_counter,
)
from openplan.plannen.models.factories.overkoepelendplan import (
    OverkoepelendPlanFactory,
)
from openplan.plannen.models.factories.plan import PlanFactory
from openplan.plannen.models.factories.plantype import PlanTypeFactory

from ...models.plan import Plan
from .api_testcase import APITestCase


class PlanAPITests(APITestCase):
    def setUp(self):
        super().setUp()
        self.plantype1 = PlanTypeFactory.create()
        self.plantype2 = PlanTypeFactory.create()
        self.over_plan1 = OverkoepelendPlanFactory.create()
        self.over_plan2 = OverkoepelendPlanFactory.create()

    def test_create_plan(self):
        plantype = PlanTypeFactory.create()
        overkoepelend_plan = OverkoepelendPlanFactory.create()

        url = reverse("plannen:plan-list")
        data = {
            "titel": "Test Instrument",
            "startdatum": date.today().isoformat(),
            "plantypeUuid": str(plantype.uuid),
            "overkoepelendPlanUuid": str(overkoepelend_plan.uuid),
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        plan = Plan.objects.get(uuid=response.data["uuid"])
        self.assertEqual(plan.plantype.uuid, plantype.uuid)

    def test_list_plans(self):
        plantype = PlanTypeFactory.create()
        PlanFactory.create_batch(3, plantype=plantype)

        url = reverse("plannen:plan-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()["results"]
        self.assertEqual(len(data), 3)

        for plan_data in data:
            self.assertIn("uuid", plan_data)
            self.assertIn("plantype", plan_data)

    def test_retrieve_plan(self):
        plantype = PlanTypeFactory.create()
        plan = PlanFactory.create(plantype=plantype)

        url = reverse("plannen:plan-detail", kwargs={"uuid": plan.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(plan.uuid))
        self.assertEqual(response.data["plantype"]["type"], str(plan.plantype))

    def test_update_plan(self):
        plantype = PlanTypeFactory.create()
        overkoepelend_plan = OverkoepelendPlanFactory.create()
        plan = PlanFactory.create(
            plantype=plantype, overkoepelend_plan=overkoepelend_plan
        )
        new_plantype = PlanTypeFactory.create()

        url = reverse("plannen:plan-detail", kwargs={"uuid": plan.uuid})
        data = {
            "titel": "Test update instrument",
            "startdatum": date.today().isoformat(),
            "plantypeUuid": str(new_plantype.uuid),
            "overkoepelendPlanUuid": str(overkoepelend_plan.uuid),
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plan.refresh_from_db()
        self.assertEqual(plan.plantype.uuid, new_plantype.uuid)

    def test_partial_update_plan(self):
        plantype = PlanTypeFactory.create()
        plan = PlanFactory.create(plantype=plantype)
        new_plantype = PlanTypeFactory.create()

        url = reverse("plannen:plan-detail", kwargs={"uuid": plan.uuid})
        data = {"plantypeUuid": str(new_plantype.uuid)}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plan.refresh_from_db()
        self.assertEqual(plan.plantype.uuid, new_plantype.uuid)

    def test_delete_plan(self):
        plantype = PlanTypeFactory.create()
        plan = PlanFactory.create(plantype=plantype)

        url = reverse("plannen:plan-detail", kwargs={"uuid": plan.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Plan.objects.filter(uuid=plan.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen:plan-list")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_plantype_uuid(self):
        plan1 = PlanFactory.create(plantype=self.plantype1)
        PlanFactory.create(plantype=self.plantype2)

        url = reverse("plannen:plan-list")
        response = self.client.get(url, {"plantype__uuid": str(self.plantype1.uuid)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

    def test_filter_overkoepelend_plan_uuid(self):
        plan1 = PlanFactory.create(overkoepelend_plan=self.over_plan1)
        PlanFactory.create(overkoepelend_plan=self.over_plan2)

        url = reverse("plannen:plan-list")
        response = self.client.get(
            url, {"overkoepelend_plan__uuid": str(self.over_plan1.uuid)}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

    def test_filter_status(self):
        plan1 = PlanFactory.create(status=PlanStatus.ACTIEF)
        PlanFactory.create(status=PlanStatus.AFGEROND)

        url = reverse("plannen:plan-list")
        response = self.client.get(url, {"status": "actief"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

    def test_filter_fase(self):
        plan1 = PlanFactory.create(fase=PlanStatus.ACTIEF)
        PlanFactory.create(fase=PlanStatus.AFGEROND)

        url = reverse("plannen:plan-list")
        response = self.client.get(url, {"fase": "actief"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

    def test_filter_titel(self):
        plan1 = PlanFactory.create(titel="Project Start")
        PlanFactory.create(titel="Project End")

        url = reverse("plannen:plan-list")
        with self.subTest("exact"):
            response = self.client.get(url, {"titel": "Project Start"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

        with self.subTest("icontains"):
            response = self.client.get(url, {"titel__icontains": "Start"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

    def test_filter_medewerker(self):
        plan1 = PlanFactory.create(medewerker="urn:example:zaak:1")
        PlanFactory.create(medewerker="urn:example:zaak:2")

        url = reverse("plannen:plan-list")
        response = self.client.get(url, {"medewerker": "urn:example:zaak:1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

    def test_filter_zaak(self):
        plan1 = PlanFactory.create(zaak="urn:example:zaak:1")
        PlanFactory.create(zaak="urn:example:zaak:2")

        url = reverse("plannen:plan-list")
        response = self.client.get(url, {"zaak": "urn:example:zaak:1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

    def test_filter_domeinregister(self):
        plan1 = PlanFactory.create(domeinregister="urn:example:domein:1")
        PlanFactory.create(domeinregister="urn:example:domein:2")

        url = reverse("plannen:plan-list")
        response = self.client.get(url, {"domeinregister": "urn:example:domein:1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

    def test_startdatum_filter(self):
        plan1 = PlanFactory.create(startdatum=timezone.make_aware(datetime(2026, 1, 1)))
        PlanFactory.create(startdatum=timezone.make_aware(datetime(2026, 2, 1)))

        url = reverse("plannen:plan-list")
        with self.subTest("exact"):
            response = self.client.get(url, {"startdatum": "2026-01-01"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

        with self.subTest("lte"):
            response = self.client.get(url, {"startdatum__lte": "2026-01-31"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)

        with self.subTest("gte"):
            response = self.client.get(url, {"startdatum__gte": "2026-02-01"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)

    def test_einddatum_filter(self):
        plan1 = PlanFactory.create(
            startdatum=timezone.make_aware(datetime(2026, 1, 1)),
            einddatum=timezone.make_aware(datetime(2026, 1, 15)),
        )
        PlanFactory.create(
            startdatum=timezone.make_aware(datetime(2026, 2, 1)),
            einddatum=timezone.make_aware(datetime(2026, 2, 15)),
        )

        url = reverse("plannen:plan-list")
        with self.subTest("exact"):
            response = self.client.get(url, {"einddatum": "2026-01-15"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

        with self.subTest("lte"):
            response = self.client.get(url, {"einddatum__lte": "2026-01-31"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)

        with self.subTest("gte"):
            response = self.client.get(url, {"einddatum__gte": "2026-02-01"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)

    def test_plan_urn(self):
        plantype = PlanTypeFactory.create()
        plan = PlanFactory.create(plantype=plantype)

        url = reverse("plannen:plan-detail", kwargs={"uuid": plan.uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["urn"], f"urn:maykin:plannen:plan:{str(plan.uuid)}"
        )

    def test_invalid_create_urn_fields_plan(self):
        self.assertFalse(Plan.objects.exists())

        plantype = PlanTypeFactory.create()
        data = {
            "titel": "Test Plan",
            "plantype": str(plantype.uuid),
            "zaak": "invalid",
            "domeinregister": "urn:maykinmaykinmaykinmaykinmaykinmaykinmaykinmaykinmaykin:1",
            "medewerker": "test:maykin:organisatie:medewerker:1234567892",
        }

        url = reverse("plannen:plan-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            get_validation_errors(response, "zaak"),
            {
                "name": "zaak",
                "code": "invalid_urn",
                "reason": "Enter a valid URN. Correct format: 'urn:<namespace>:<resource>' (e.g., urn:isbn:9780143127796).",
            },
        )
        self.assertEqual(
            get_validation_errors(response, "domeinregister"),
            {
                "name": "domeinregister",
                "code": "invalid_urn",
                "reason": "Enter a valid URN. Correct format: 'urn:<namespace>:<resource>' (e.g., urn:isbn:9780143127796).",
            },
        )
        self.assertEqual(
            get_validation_errors(response, "medewerker"),
            {
                "name": "medewerker",
                "code": "invalid_urn",
                "reason": "Enter a valid URN. Correct format: 'urn:<namespace>:<resource>' (e.g., urn:isbn:9780143127796).",
            },
        )
        self.assertFalse(Plan.objects.exists())

    @patch.object(plannen_create_counter, "add", wraps=plannen_create_counter.add)
    def test_create_plan_increments_metric(self, mock_add: MagicMock):
        plantype = PlanTypeFactory.create()
        overkoepelend_plan = OverkoepelendPlanFactory.create()
        url = reverse("plannen:plan-list")
        data = {
            "titel": "Test Instrument",
            "startdatum": date.today().isoformat(),
            "plantypeUuid": str(plantype.uuid),
            "overkoepelendPlanUuid": str(overkoepelend_plan.uuid),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        mock_add.assert_called_once_with(1)

    @patch.object(plannen_update_counter, "add", wraps=plannen_update_counter.add)
    def test_update_plan_increments_metric(self, mock_add: MagicMock):
        plantype = PlanTypeFactory.create()
        plan = PlanFactory.create(plantype=plantype)
        new_plantype = PlanTypeFactory.create()
        url = reverse("plannen:plan-detail", kwargs={"uuid": plan.uuid})
        data = {"plantypeUuid": str(new_plantype.uuid)}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        mock_add.assert_called_once_with(1)

    @patch.object(plannen_delete_counter, "add", wraps=plannen_delete_counter.add)
    def test_delete_plan_increments_metric(self, mock_add: MagicMock):
        plantype = PlanTypeFactory.create()
        plan = PlanFactory.create(plantype=plantype)
        url = reverse("plannen:plan-detail", kwargs={"uuid": plan.uuid})
        response = self.client.delete(url)
        self.assertIn(response.status_code, (200, 204))
        mock_add.assert_called_once_with(1)
