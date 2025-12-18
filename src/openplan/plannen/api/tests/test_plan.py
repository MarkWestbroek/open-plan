from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from openplan.plannen.models.factories.plan import PlanFactory
from openplan.plannen.models.factories.plantype import PlanTypeFactory

from ...models.plan import Plan
from .api_testcase import APITestCase


class PlanAPITests(APITestCase):
    def test_create_plan(self):
        plantype = PlanTypeFactory.create()

        url = reverse("plannen_api:plan-list")
        data = {"plantypeUuid": str(plantype.uuid)}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        plan = Plan.objects.get(uuid=response.data["uuid"])
        self.assertEqual(plan.plantype.uuid, plantype.uuid)

    def test_list_plans(self):
        plantype = PlanTypeFactory.create()
        PlanFactory.create_batch(3, plantype=plantype)

        url = reverse("plannen_api:plan-list")
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

        url = reverse("plannen_api:plan-detail", kwargs={"uuid": plan.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(plan.uuid))
        self.assertEqual(response.data["plantype"]["type"], str(plan.plantype))

    def test_update_plan(self):
        plantype = PlanTypeFactory.create()
        plan = PlanFactory.create(plantype=plantype)
        new_plantype = PlanTypeFactory.create()

        url = reverse("plannen_api:plan-detail", kwargs={"uuid": plan.uuid})
        data = {"plantypeUuid": str(new_plantype.uuid)}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plan.refresh_from_db()
        self.assertEqual(plan.plantype.uuid, new_plantype.uuid)

    def test_partial_update_plan(self):
        plantype = PlanTypeFactory.create()
        plan = PlanFactory.create(plantype=plantype)
        new_plantype = PlanTypeFactory.create()

        url = reverse("plannen_api:plan-detail", kwargs={"uuid": plan.uuid})
        data = {"plantypeUuid": str(new_plantype.uuid)}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plan.refresh_from_db()
        self.assertEqual(plan.plantype.uuid, new_plantype.uuid)

    def test_delete_plan(self):
        plantype = PlanTypeFactory.create()
        plan = PlanFactory.create(plantype=plantype)

        url = reverse("plannen_api:plan-detail", kwargs={"uuid": plan.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Plan.objects.filter(uuid=plan.uuid).exists())

    def test_authentication_required(self):
        client = APIClient()
        url = reverse("plannen_api:plan-list")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_plantype_uuid(self):
        type1 = PlanTypeFactory()
        type2 = PlanTypeFactory()

        plan1 = PlanFactory(plantype=type1)
        PlanFactory(plantype=type2)

        url = reverse("plannen_api:plan-list")
        response = self.client.get(url, {"plantype_uuid": str(type1.uuid)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], str(plan1.uuid))
