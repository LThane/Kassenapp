import reflex as rx
from app.components.auth_layout import auth_layout
from app.states.auth_state import MyAuthState


def login_page() -> rx.Component:
    """The login page."""
    return auth_layout(
        rx.el.div(
            rx.el.h2(
                "Sign in to your account", class_name="text-2xl font-bold text-gray-900"
            ),
            rx.el.p("Welcome back!", class_name="text-gray-600 mt-1"),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Email", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        type="email",
                        id="email",
                        placeholder="you@example.com",
                        required=True,
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:ring-violet-500 focus:border-violet-500",
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
                        placeholder="••••••••",
                        required=True,
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:ring-violet-500 focus:border-violet-500",
                    ),
                    class_name="space-y-1",
                ),
                rx.el.button(
                    "Sign In",
                    type="submit",
                    class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-violet-600 hover:bg-violet-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500",
                ),
                class_name="space-y-6",
                on_submit=MyAuthState.on_login,
            ),
            rx.el.p(
                "Don't have an account? ",
                rx.el.a(
                    "Sign up",
                    href="/register",
                    class_name="font-medium text-violet-600 hover:text-violet-500",
                ),
                class_name="mt-4 text-center text-sm text-gray-600",
            ),
            class_name="space-y-6",
        )
    )