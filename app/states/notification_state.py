import reflex as rx
from sqlmodel import select
from .base_state import BaseState
from app.models import Notification
from .auth_state import MyAuthState
from app.database import db_session
from datetime import datetime
from typing import cast


class NotificationState(BaseState):
    notifications: list[Notification] = []
    show_notifications: bool = False

    def _is_notification_unread(self, notification: Notification | dict) -> bool:
        """Safely checks if a notification is unread, handling both objects and dicts."""
        if isinstance(notification, dict):
            return not notification.get("is_read", True)
        return not notification.is_read

    @rx.var
    def unread_count(self) -> int:
        return sum((1 for n in self.notifications if self._is_notification_unread(n)))

    @rx.event
    def toggle_notifications(self):
        self.show_notifications = not self.show_notifications

    @rx.event
    async def load_notifications(self):
        auth_state = await self.get_state(MyAuthState)
        if not auth_state.is_authenticated:
            return
        current_user = auth_state.current_user
        member_id = (
            current_user["id"] if isinstance(current_user, dict) else current_user.id
        )
        if not member_id:
            return
        with db_session() as session:
            results = session.exec(
                select(Notification)
                .where(Notification.member_id == member_id)
                .order_by(Notification.created_at.desc())
                .limit(20)
            ).all()
            self.notifications = results

    @rx.event
    def mark_as_read(self, notification_id: int):
        with db_session() as session:
            db_notification = session.get(Notification, notification_id)
            if db_notification and (not db_notification.is_read):
                db_notification.is_read = True
                session.add(db_notification)
                session.commit()
                session.refresh(db_notification)
                for i, n in enumerate(self.notifications):
                    if n.id == notification_id:
                        self.notifications[i] = db_notification
                        break

    @rx.event
    async def mark_all_as_read(self):
        auth_state = await self.get_state(MyAuthState)
        if not auth_state.is_authenticated:
            return
        current_user = auth_state.current_user
        member_id = (
            current_user["id"] if isinstance(current_user, dict) else current_user.id
        )
        if not member_id:
            return
        with db_session() as session:
            unread_notifications = session.exec(
                select(Notification).where(
                    Notification.member_id == member_id, Notification.is_read == False
                )
            ).all()
            for notification in unread_notifications:
                notification.is_read = True
                session.add(notification)
            if unread_notifications:
                session.commit()
        yield NotificationState.load_notifications