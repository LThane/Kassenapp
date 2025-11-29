import reflex as rx
from app.pages.index import index
from app.pages.login import login_page
from app.pages.register import register_page
from app.pages.profile import profile_page
from app.pages.costs import costs_page
from app.pages.all_costs import all_costs_page
from app.pages.quick_entry import quick_entry_page
from app.pages.tile_entry import tile_entry_page
from app.states.auth_state import MyAuthState
from app.states.notification_state import NotificationState
from app.database import init_db

init_db()
app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(profile_page, route="/profile")
app.add_page(costs_page, route="/costs")
app.add_page(all_costs_page, route="/all-costs")
app.add_page(quick_entry_page, route="/quick-entry")
app.add_page(tile_entry_page, route="/tile-entry")