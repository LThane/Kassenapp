import reflex as rx
from sqlmodel import select
from .base_state import BaseState
from app.models import Member, Cost
from app.database import db_session
from datetime import datetime
import logging


class QuickEntryState(BaseState):
    members: list[Member] = []
    categories: dict[str, float | None] = {
        "Getränke (nicht-alkoholisch) - €1.50": 1.5,
        "Getränke (alkoholisch) - €2.50": 2.5,
        "Anderes": None,
    }
    form_states: dict[int, dict[str, str]] = {}

    @rx.var
    def today_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    @rx.event
    def get_all_members(self):
        with db_session() as session:
            self.members = session.exec(
                select(Member)
                .where(Member.email != "acf@admin.com")
                .order_by(Member.name)
            ).all()
            for member in self.members:
                if member.id not in self.form_states:
                    self.form_states[member.id] = {
                        "category": "",
                        "amount": "",
                        "description": "",
                        "date": self.today_date,
                    }

    @rx.var
    def get_form_state(self) -> dict[int, dict[str, str]]:
        return self.form_states

    @rx.event
    def set_form_field(self, member_id: int, field: str, value: str):
        if member_id not in self.form_states:
            self.form_states[member_id] = {}
        self.form_states[member_id][field] = value
        if field == "category":
            category_price = self.categories.get(value)
            if category_price is not None:
                self.form_states[member_id]["amount"] = str(category_price)
            elif value != "Anderes":
                self.form_states[member_id]["amount"] = ""

    @rx.event
    def add_cost_for_member(self, member_id: int):
        form_data = self.form_states.get(member_id, {})
        category = form_data.get("category", "")
        amount_str = form_data.get("amount", "")
        date = form_data.get("date", self.today_date)
        description = form_data.get("description", "")
        if not category:
            return rx.toast.error("Category is required.")
        amount: float
        category_value = self.categories.get(category)
        if category == "Anderes":
            if not amount_str:
                return rx.toast.error("Amount is required for 'Anderes' category.")
            try:
                amount = float(amount_str)
            except (ValueError, TypeError) as e:
                logging.exception(f"Error converting amount to float: {e}")
                return rx.toast.error("Invalid amount.")
        elif category_value is not None:
            amount = category_value
        else:
            return rx.toast.error("Invalid category selected.")
        with db_session() as session:
            new_cost = Cost(
                description=description,
                amount=amount,
                date=date,
                category=category,
                member_id=member_id,
            )
            session.add(new_cost)
            session.commit()
        self.form_states[member_id] = {
            "category": "",
            "amount": "",
            "description": "",
            "date": self.today_date,
        }
        return rx.toast.success(f"Cost added for member ID {member_id}")