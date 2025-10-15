import reflex as rx
from app.components.navbar import main_layout
from app.states.auth_state import MyAuthState


def index() -> rx.Component:
    return main_layout(
        rx.cond(
            MyAuthState.is_authenticated,
            rx.el.div(
                rx.el.h1(
                    f"Welcome, {MyAuthState.current_user.name}!",
                    class_name="text-3xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Manage your expenses and view your profile.",
                    class_name="mt-2 text-gray-600",
                ),
                rx.el.a(
                    rx.el.button(
                        "Go to Dashboard",
                        class_name="mt-6 bg-violet-600 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-violet-700 transition-colors shadow-sm",
                    ),
                    href="/costs",
                ),
                class_name="p-8 bg-white rounded-xl border border-gray-200 shadow-sm",
            ),
            rx.el.div(
                rx.el.h1(
                    "Please log in to continue.",
                    class_name="text-3xl font-bold text-gray-900",
                ),
                class_name="p-8 bg-white rounded-xl border border-gray-200 shadow-sm",
            ),
        )
    )