import reflex as rx
from app.components.auth_layout import auth_layout
from app.states.acf_state import ACFState


def acf_login_page() -> rx.Component:
    """The ACF login page."""
    return auth_layout(
        rx.el.div(
            rx.el.h2(
                "ACF Quick Entry Login", class_name="text-2xl font-bold text-gray-900"
            ),
            rx.el.p("Special access for cost entry.", class_name="text-gray-600 mt-1"),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Username", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        type="text",
                        id="username",
                        placeholder="ACF",
                        required=True,
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm text-gray-800 shadow-sm placeholder-gray-400 focus:outline-none focus:ring-violet-500 focus:border-violet-500",
                    ),
                    class_name="space-y-1",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        type="password",
                        id="password",
                        placeholder="•••",
                        required=True,
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm text-gray-800 shadow-sm placeholder-gray-400 focus:outline-none focus:ring-violet-500 focus:border-violet-500",
                    ),
                    class_name="space-y-1",
                ),
                rx.el.button(
                    "Login",
                    type="submit",
                    class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-violet-600 hover:bg-violet-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500",
                ),
                class_name="space-y-6",
                on_submit=ACFState.acf_login,
            ),
            class_name="space-y-6",
        )
    )