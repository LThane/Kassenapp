import reflex as rx
from sqlmodel import select
from .base_state import BaseState
from app.models import Member, Cost, Notification
from .auth_state import MyAuthState
from app.database import db_session
from datetime import datetime
import logging


class QuickEntryState(BaseState):
    members: list[Member] = []
    search_query: str = ""
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
    def set_search_query(self, query: str):
        """Sets the search query for filtering members."""
        self.search_query = query

    @rx.var
    def filtered_members(self) -> list[Member]:
        """Filters members based on the search query."""
        if not self.search_query.strip():
            return self.members
        query = self.search_query.lower()
        return [member for member in self.members if query in member.name.lower()]

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
    async def add_cost_for_member(self, member_id: int):
        auth_state = await self.get_state(MyAuthState)
        if not auth_state.is_authenticated:
            yield rx.toast.error("You must be logged in.")
            return
        form_data = self.form_states.get(member_id, {})
        category = form_data.get("category", "")
        amount_str = form_data.get("amount", "")
        date = form_data.get("date", self.today_date)
        description = form_data.get("description", "")
        if not category:
            yield rx.toast.error("Category is required.")
            return
        amount: float
        category_value = self.categories.get(category)
        if category == "Anderes":
            if not amount_str:
                yield rx.toast.error("Amount is required for 'Anderes' category.")
                return
            try:
                amount = float(amount_str)
            except (ValueError, TypeError) as e:
                logging.exception(f"Error converting amount to float: {e}")
                yield rx.toast.error("Invalid amount.")
                return
        elif category_value is not None:
            amount = category_value
        else:
            yield rx.toast.error("Invalid category selected.")
            return
        with db_session() as session:
            new_cost = Cost(
                description=description,
                amount=amount,
                date=date,
                category=category,
                member_id=member_id,
            )
            session.add(new_cost)
            member_name = ""
            for m in self.members:
                if m.id == member_id:
                    member_name = m.name.split()[0]
                    break
            if auth_state.current_user.id != member_id:
                notification_message = f"{auth_state.current_user.name} hat Kosten (€{amount:.2f}) für dich hinzugefügt."
                new_notification = Notification(
                    member_id=member_id, message=notification_message
                )
                session.add(new_notification)
                yield rx.toast.info(f"Benachrichtigung an {member_name} gesendet.")
            session.commit()
        self.form_states[member_id] = {
            "category": "",
            "amount": "",
            "description": "",
            "date": self.today_date,
        }
        yield rx.toast.success(f"Cost added for {member_name}!")
        return

    @rx.event
    async def add_quick_drink_for_member(self, member_id: int, drink_type: str):
        auth_state = await self.get_state(MyAuthState)
        if not auth_state.is_authenticated:
            yield rx.toast.error("You must be logged in.")
            return
        if drink_type == "non-alcoholic":
            category = "Getränke (nicht-alkoholisch) - €1.50"
            amount = 1.5
            description = "Nicht-alkoholisches Getränk"
        elif drink_type == "alcoholic":
            category = "Getränke (alkoholisch) - €2.50"
            amount = 2.5
            description = "Alkoholisches Getränk"
        else:
            yield rx.toast.error("Invalid drink type.")
            return
        with db_session() as session:
            new_cost = Cost(
                description=description,
                amount=amount,
                date=self.today_date,
                category=category,
                member_id=member_id,
            )
            session.add(new_cost)
            member_name = ""
            for m in self.members:
                if m.id == member_id:
                    member_name = m.name.split()[0]
                    break
            if auth_state.current_user.id != member_id:
                notification_message = f"{auth_state.current_user.name} hat ein '{description}' für dich hinzugefügt."
                new_notification = Notification(
                    member_id=member_id, message=notification_message
                )
                session.add(new_notification)
                yield rx.toast.info(f"Benachrichtigung an {member_name} gesendet.")
            session.commit()
        yield rx.toast.success(f"Drink added for {member_name}!")