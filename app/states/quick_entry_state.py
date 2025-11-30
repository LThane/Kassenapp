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
    open_forms: list[int] = []
    selected_member_id: int = -1
    is_selection_open: bool = False
    is_custom_form_visible: bool = False
    show_confirmation: bool = False
    confirmation_details: dict[str, str] = {
        "member_name": "",
        "item_name": "",
        "amount": "",
    }
    last_booking_id: int = -1
    last_notification_id: int = -1
    last_booking_timestamp: datetime | None = None

    @rx.var
    def selected_member(self) -> Member:
        return next(
            (m for m in self.members if m.id == self.selected_member_id),
            Member(id=0, name="", email="", password=""),
        )

    @rx.event
    def open_selection(self, member_id: int):
        self.selected_member_id = member_id
        self.is_selection_open = True
        self.is_custom_form_visible = False
        if member_id not in self.form_states:
            self.form_states[member_id] = {
                "category": "",
                "amount": "",
                "description": "",
                "date": self.today_date,
            }

    @rx.event
    def close_selection(self):
        self.is_selection_open = False

    @rx.event
    def toggle_custom_form(self):
        self.is_custom_form_visible = not self.is_custom_form_visible

    @rx.event
    def close_confirmation(self):
        self.show_confirmation = False

    @rx.event
    def toggle_form(self, member_id: int):
        if member_id in self.open_forms:
            self.open_forms = [mid for mid in self.open_forms if mid != member_id]
        else:
            self.open_forms = self.open_forms + [member_id]

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
            auth_user = auth_state.current_user
            auth_user_id = (
                auth_user.get("id") if isinstance(auth_user, dict) else auth_user.id
            )
            auth_user_name = (
                auth_user.get("name") if isinstance(auth_user, dict) else auth_user.name
            )
            new_notification = None
            if auth_user_id != member_id:
                notification_message = (
                    f"{auth_user_name} hat Kosten (€{amount:.2f}) für dich hinzugefügt."
                )
                new_notification = Notification(
                    member_id=member_id, message=notification_message
                )
                session.add(new_notification)
                yield rx.toast.info(f"Benachrichtigung an {member_name} gesendet.")
            session.commit()
            session.refresh(new_cost)
            self.last_booking_id = new_cost.id
            self.last_booking_timestamp = datetime.now()
            if new_notification:
                session.refresh(new_notification)
                self.last_notification_id = new_notification.id
            else:
                self.last_notification_id = -1
        self.form_states[member_id] = {
            "category": "",
            "amount": "",
            "description": "",
            "date": self.today_date,
        }
        if member_id in self.open_forms:
            self.open_forms = [mid for mid in self.open_forms if mid != member_id]
        self.confirmation_details = {
            "member_name": member_name,
            "item_name": description if description else category,
            "amount": f"€{amount:.2f}",
        }
        self.show_confirmation = True
        self.is_selection_open = False
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
            auth_user = auth_state.current_user
            auth_user_id = (
                auth_user.get("id") if isinstance(auth_user, dict) else auth_user.id
            )
            auth_user_name = (
                auth_user.get("name") if isinstance(auth_user, dict) else auth_user.name
            )
            new_notification = None
            if auth_user_id != member_id:
                notification_message = (
                    f"{auth_user_name} hat ein '{description}' für dich hinzugefügt."
                )
                new_notification = Notification(
                    member_id=member_id, message=notification_message
                )
                session.add(new_notification)
                yield rx.toast.info(f"Benachrichtigung an {member_name} gesendet.")
            session.commit()
            session.refresh(new_cost)
            self.last_booking_id = new_cost.id
            self.last_booking_timestamp = datetime.now()
            if new_notification:
                session.refresh(new_notification)
                self.last_notification_id = new_notification.id
            else:
                self.last_notification_id = -1
        self.confirmation_details = {
            "member_name": member_name,
            "item_name": description,
            "amount": f"€{amount:.2f}",
        }
        self.show_confirmation = True
        self.is_selection_open = False
        yield rx.toast.success(f"Drink added for {member_name}!")

    @rx.event
    def undo_last_booking(self):
        if self.last_booking_id <= 0:
            return rx.toast.error("Keine Buchung zum Stornieren gefunden.")
        with db_session() as session:
            cost = session.get(Cost, self.last_booking_id)
            if cost:
                session.delete(cost)
            if self.last_notification_id > 0:
                notif = session.get(Notification, self.last_notification_id)
                if notif:
                    session.delete(notif)
            session.commit()
        self.last_booking_id = -1
        self.last_notification_id = -1
        self.last_booking_timestamp = None
        self.show_confirmation = False
        yield rx.toast.success("Buchung erfolgreich rückgängig gemacht.")