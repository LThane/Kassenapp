import reflex as rx
from sqlmodel import select
from .base_state import BaseState
from app.models import Notification
from .auth_state import MyAuthState
from app.database import db_session
from datetime import datetime


class NotificationState(BaseState):
    notifications: list[Notification] = []
    show_notifications: bool = False

    @rx.var
    def unread_count(self) -> int:
        return sum((1 for n in self.notifications if not n.is_read))

    @rx.event
    def toggle_notifications(self):
        self.show_notifications = not self.show_notifications

    @rx.event
    async def load_notifications(self):
        auth_state = await self.get_state(MyAuthState)
        if not auth_state.is_authenticated:
            return
        with db_session() as session:
            results = session.exec(
                select(Notification)
                .where(Notification.member_id == auth_state.current_user.id)
                .order_by(Notification.created_at.desc())
                .limit(20)
            ).all()
            self.notifications = results

    @rx.event
    def mark_as_read(self, notification_id: int):
        with db_session() as session:
            notification = session.get(Notification, notification_id)
            if notification and (not notification.is_read):
                notification.is_read = True
                session.add(notification)
                session.commit()
                session.refresh(notification)
        for i, n in enumerate(self.notifications):
            if n.id == notification_id:
                self.notifications[i] = notification
                break

    @rx.event
    def mark_all_as_read(self):
        with db_session() as session:
            auth_state = self.get_state_sync(MyAuthState)
            unread = session.exec(
                select(Notification).where(
                    Notification.member_id == auth_state.current_user.id,
                    Notification.is_read == False,
                )
            ).all()
            for notification in unread:
                notification.is_read = True
                session.add(notification)
            session.commit()
        return NotificationState.load_notifications