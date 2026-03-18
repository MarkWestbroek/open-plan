import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from openplan.plannen.models.factories.overkoepelendplan import OverkoepelendPlanFactory
from openplan.plannen.models.plan import Plan, PlanState
from openplan.plannen.models.plantype import PlanType
from openplan.utils.state import create_state

from ..enums.status import PlanStatus
from ..enums.type import PlanTypeEnum

User = get_user_model()


class PlanStateModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester")
        self.overplan = OverkoepelendPlanFactory()
        self.plantype = PlanType.objects.create(type=PlanTypeEnum.INKOMEN)

    def test_create_initial_state(self):
        plan = Plan.objects.create(
            overkoepelend_plan=self.overplan,
            plantype=self.plantype,
            zaak="urn:zaak:123",
            domeinregister="urn:register:abc",
            medewerker="urn:medewerker:xyz",
        )

        state = create_state(
            stable_obj=plan,
            state_model=PlanState,
            user=self.user,
            startdatum=timezone.make_aware(datetime.datetime(2026, 1, 1, 10, 0)),
            titel="Initieel Plan",
            notitie="Eerste versie",
            status="ACTIEF",
            fase="START",
            reden_einde="",
        )

        self.assertEqual(plan.current_state.titel, "Initieel Plan")
        self.assertEqual(plan.states.count(), 1)
        self.assertIsNone(state.einddatum)

    def test_create_second_state_closes_first(self):
        plan = Plan.objects.create(
            overkoepelend_plan=self.overplan,
            plantype=self.plantype,
        )

        state1 = create_state(
            stable_obj=plan,
            state_model=PlanState,
            user=self.user,
            startdatum=timezone.make_aware(datetime.datetime(2026, 1, 1, 10, 0)),
            titel="Initieel Plan",
            notitie="Eerste versie",
            status="ACTIEF",
            fase="START",
            reden_einde="",
        )

        state2 = create_state(
            stable_obj=plan,
            state_model=PlanState,
            user=self.user,
            startdatum=timezone.make_aware(datetime.datetime(2026, 2, 1, 10, 0)),
            titel="Tweede Plan",
            notitie="Update versie",
            status="ACTIEF",
            fase="MID",
            reden_einde="",
        )

        # state1 moet automatisch afgesloten zijn
        state1.refresh_from_db()
        self.assertEqual(
            state1.einddatum, timezone.make_aware(datetime.datetime(2026, 2, 1, 10, 0))
        )

        # current_state is nu state2
        self.assertEqual(plan.current_state.titel, "Tweede Plan")
        self.assertEqual(plan.states.count(), 2)

    def test_at_date_query(self):
        plan = Plan.objects.create(
            overkoepelend_plan=self.overplan,
            plantype=self.plantype,
        )

        create_state(
            stable_obj=plan,
            state_model=PlanState,
            user=self.user,
            startdatum=timezone.make_aware(datetime.datetime(2026, 1, 1, 10, 0)),
            titel="Initieel Plan",
            status=PlanStatus.ACTIEF,
            fase="START",
        )
        create_state(
            stable_obj=plan,
            state_model=PlanState,
            user=self.user,
            startdatum=timezone.make_aware(datetime.datetime(2026, 2, 1, 10, 0)),
            titel="Tweede Plan",
            status=PlanStatus.AFGEROND,
            fase="MID",
        )

        s1 = plan.states.at(
            timezone.make_aware(datetime.datetime(2026, 1, 1, 10, 0))
        ).first()
        s2 = plan.states.at(
            timezone.make_aware(datetime.datetime(2026, 2, 1, 10, 0))
        ).first()

        self.assertEqual(s1.titel, "Initieel Plan")
        self.assertEqual(s2.titel, "Tweede Plan")

    def test_history_ordering(self):
        plan = Plan.objects.create(
            overkoepelend_plan=self.overplan,
            plantype=self.plantype,
        )

        create_state(
            stable_obj=plan,
            state_model=PlanState,
            user=self.user,
            startdatum=timezone.make_aware(datetime.datetime(2026, 1, 1, 10, 0)),
            titel="State1",
            status=PlanStatus.ACTIEF,
        )
        create_state(
            stable_obj=plan,
            state_model=PlanState,
            user=self.user,
            startdatum=timezone.make_aware(datetime.datetime(2026, 2, 1, 10, 0)),
            titel="State2",
            status=PlanStatus.AFGEROND,
        )

        history = plan.states.history()
        for state in history:
            print(
                f"ID: {state.id}, Titel: {state.titel}, "
                f"Start: {state.startdatum}, Eind: {state.einddatum}, Status: {state.status}"
            )

        self.assertEqual([s.titel for s in history], ["State1", "State2"])
