import reflex as rx
from app.components.navbar import main_layout
from app.states.auth_state import MyAuthState


def profile_page() -> rx.Component:
    """Member profile page."""
    return main_layout(
        rx.el.div(
            rx.el.h1("Member Profile", class_name="text-3xl font-bold text-gray-900"),
            rx.cond(
                MyAuthState.is_authenticated & (MyAuthState.current_user.id != 0),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=f"https://api.dicebear.com/9.x/initials/svg?seed={MyAuthState.current_user.name}",
                                class_name="h-24 w-24 rounded-full",
                            ),
                            class_name="flex-shrink-0",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                MyAuthState.current_user.name,
                                class_name="text-xl font-semibold text-gray-800",
                            ),
                            rx.el.p(
                                MyAuthState.current_user.email,
                                class_name="text-gray-500",
                            ),
                            class_name="mt-4 md:mt-0 md:ml-6",
                        ),
                        class_name="md:flex items-center",
                    ),
                    class_name="mt-8",
                ),
                rx.el.div(rx.el.p("Loading profile...", class_name="text-gray-500")),
            ),
            class_name="p-8 bg-white rounded-xl border border-gray-200 shadow-sm",
        )
    )