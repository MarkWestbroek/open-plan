from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from vng_api_common.tests import get_validation_errors

from openplan.plannen.models.factories.plan import PlanFactory
from openplan.plannen.models.factories.plantype import PlanTypeFactory

from ...models.plan import Plan
from .api_testcase import APITestCase


class PlanAPITests(APITestCase):
    def test_create_plan(self):
        plantype = PlanTypeFactory.create()

        url = reverse("plannen:plan-list")
        data = {"plantypeUuid": str(plantype.uuid)}
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
        plan = PlanFactory.create(plantype=plantype)
        new_plantype = PlanTypeFactory.create()

        url = reverse("plannen:plan-detail", kwargs={"uuid": plan.uuid})
        data = {"plantypeUuid": str(new_plantype.uuid)}
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
        type1 = PlanTypeFactory()
        type2 = PlanTypeFactory()

        plan1 = PlanFactory(plantype=type1)
        PlanFactory(plantype=type2)

        url = reverse("plannen:plan-list")
        response = self.client.get(url, {"plantype_uuid": str(type1.uuid)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))

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
