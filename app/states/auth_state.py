import reflex as rx
import bcrypt
from sqlmodel import select
from .base_state import BaseState
from app.models import Member, RegisterForm, LoginForm
from app.database import db_session


class MyAuthState(BaseState):
    is_authenticated: bool = False
    current_user: Member = Member(id=0, name="", email="", password="")

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    @rx.event
    def on_register(self, form_data: dict):
        """Register the user and log them in."""
        form = RegisterForm(
            name=form_data.get("name", ""),
            email=form_data.get("email", ""),
            password=form_data.get("password", ""),
        )
        with db_session() as session:
            existing_user = session.exec(
                select(Member).where(Member.email == form["email"])
            ).first()
            if existing_user:
                yield rx.toast.error("Email already in use.")
                return
            hashed_password = self._hash_password(form["password"])
            new_member = Member(
                name=form["name"], email=form["email"], password=hashed_password
            )
            session.add(new_member)
            session.commit()
            session.refresh(new_member)
            self.is_authenticated = True
            self.current_user = new_member
        return rx.redirect("/")

    @rx.event
    def on_login(self, form_data: dict):
        """Log the user in."""
        form = LoginForm(
            email=form_data.get("email", ""), password=form_data.get("password", "")
        )
        with db_session() as session:
            user = session.exec(
                select(Member).where(Member.email == form["email"])
            ).first()
        if user and self._verify_password(form["password"], user.password):
            self.is_authenticated = True
            self.current_user = user
            return rx.redirect("/")
        else:
            yield rx.toast.error("Invalid email or password.")

    @rx.event
    def on_logout(self) -> rx.event.EventSpec:
        """Log the user out."""
        self.is_authenticated = False
        self.current_user = Member(id=0, name="", email="", password="")
        return rx.redirect("/login")