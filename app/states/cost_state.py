import reflex as rx
import logging
from sqlmodel import select
from .base_state import BaseState
from app.models import Cost, CostForm
from .auth_state import MyAuthState
from app.database import db_session
from datetime import datetime


class CostState(BaseState):
    costs: list[dict] = []
    categories: dict[str, float | None] = {
        "Getränke (nicht-alkoholisch) - €1.50": 1.5,
        "Getränke (alkoholisch) - €2.50": 2.5,
        "Anderes": None,
    }
    form_category: str = ""
    form_amount: str = ""

    @rx.var
    def total_spent(self) -> float:
        if not self.costs:
            return 0.0
        return sum((c["amount"] for c in self.costs))

    @rx.var
    def total_costs(self) -> int:
        return len(self.costs)

    @rx.var
    def average_cost(self) -> float:
        return self.total_spent / self.total_costs if self.total_costs > 0 else 0.0

    @rx.var
    def today_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    @rx.var
    def is_custom_category(self) -> bool:
        return self.form_category == "Anderes"

    @rx.event
    async def get_costs(self):
        auth_state = await self.get_state(MyAuthState)
        if not auth_state.is_authenticated:
            return
        member_id = auth_state.current_user.id
        with db_session() as session:
            results = session.exec(
                select(Cost)
                .where(Cost.member_id == member_id)
                .order_by(Cost.date.desc())
            ).all()
            self.costs = [cost.model_dump() for cost in results]

    @rx.event
    async def add_cost(self, form_data: dict):
        auth_state = await self.get_state(MyAuthState)
        if not auth_state.is_authenticated:
            yield rx.toast.error("You must be logged in to add a cost.")
            return
        form = CostForm(
            description=form_data.get("description"),
            amount=form_data.get("amount"),
            date=form_data.get("date", ""),
            category=form_data.get("category", ""),
        )
        if not form["date"] or not form["category"]:
            yield rx.toast.error("Date and Category are required.")
            return
        amount: float
        category_value = self.categories.get(form["category"])
        if form["category"] == "Anderes":
            if not form["amount"]:
                yield rx.toast.error("Amount is required for Anderes category.")
                return
            try:
                amount = float(form["amount"])
            except (ValueError, TypeError) as e:
                logging.exception(f"Error converting amount to float: {e}")
                yield rx.toast.error("Invalid amount. Please enter a number.")
                return
        elif category_value is not None:
            amount = category_value
        else:
            yield rx.toast.error("Invalid category selected.")
            return
        with db_session() as session:
            new_cost = Cost(
                description=form["description"],
                amount=amount,
                date=form["date"],
                category=form["category"],
                member_id=auth_state.current_user.id,
            )
            session.add(new_cost)
            session.commit()
        self.form_category = ""
        self.form_amount = ""
        yield CostState.get_costs
        yield rx.toast.success("Cost added successfully!")

    @rx.event
    def delete_cost(self, cost_id: int):
        with db_session() as session:
            cost_to_delete = session.get(Cost, cost_id)
            if cost_to_delete:
                session.delete(cost_to_delete)
                session.commit()
        yield CostState.get_costs
        yield rx.toast.info("Cost deleted.")