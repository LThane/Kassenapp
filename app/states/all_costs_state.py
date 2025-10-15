import reflex as rx
import logging
from sqlmodel import select
from .base_state import BaseState
from app.models import Cost, Member, CostWithMember
from .auth_state import MyAuthState
from app.database import db_session
from collections import defaultdict
from datetime import datetime, timedelta


class AllCostsState(BaseState):
    all_costs: list[CostWithMember] = []

    @rx.var
    def total_spent_all(self) -> float:
        if not self.all_costs:
            return 0.0
        return sum((c["amount"] for c in self.all_costs))

    @rx.var
    def total_costs_all(self) -> int:
        return len(self.all_costs)

    @rx.var
    def average_cost_all(self) -> float:
        return (
            self.total_spent_all / self.total_costs_all
            if self.total_costs_all > 0
            else 0.0
        )

    @rx.var
    def total_members(self) -> int:
        if not self.all_costs:
            return 0
        return len({c["member_id"] for c in self.all_costs})

    @rx.var
    def costs_by_week_and_member(
        self,
    ) -> list[tuple[str, list[tuple[str, list[CostWithMember], float]], float]]:
        grouped = defaultdict(lambda: defaultdict(list))
        for cost in self.all_costs:
            try:
                cost_date = datetime.strptime(cost["date"], "%Y-%m-%d")
                start_of_week = cost_date - timedelta(days=cost_date.weekday())
                week_key = start_of_week.strftime("%Y-%m-%d")
                grouped[week_key][cost["member_name"]].append(cost)
            except ValueError as e:
                logging.exception(f"Error parsing date for cost: {cost}. Error: {e}")
                continue
        result = []
        sorted_weeks = sorted(grouped.keys(), reverse=True)
        for week in sorted_weeks:
            week_total = 0.0
            members_data = []
            sorted_members = sorted(grouped[week].keys())
            for member_name in sorted_members:
                member_costs = grouped[week][member_name]
                member_costs.sort(key=lambda x: x["date"], reverse=True)
                member_subtotal = sum((c["amount"] for c in member_costs))
                members_data.append((member_name, member_costs, member_subtotal))
                week_total += member_subtotal
            result.append((week, members_data, week_total))
        return result

    @rx.event
    async def get_all_costs(self):
        auth_state = await self.get_state(MyAuthState)
        if not auth_state.is_authenticated:
            return
        with db_session() as session:
            results = session.exec(
                select(Cost, Member.name)
                .join(Member, Cost.member_id == Member.id)
                .order_by(Cost.date.desc(), Member.name.asc())
            ).all()
            self.all_costs = [
                {
                    "id": cost.id,
                    "description": cost.description,
                    "amount": cost.amount,
                    "date": cost.date,
                    "category": cost.category,
                    "member_id": cost.member_id,
                    "member_name": member_name,
                }
                for cost, member_name in results
            ]