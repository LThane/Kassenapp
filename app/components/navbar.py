import reflex as rx
from app.states.auth_state import MyAuthState


def navbar() -> rx.Component:
    """A responsive navbar with user authentication status."""
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon("layers", size=24, class_name="text-violet-600"),
                    rx.el.span(
                        "AssociaCost", class_name="font-bold text-lg text-gray-800"
                    ),
                    class_name="flex items-center gap-2",
                ),
                href="/",
            ),
            rx.el.div(
                rx.cond(
                    MyAuthState.is_authenticated,
                    rx.el.div(
                        rx.el.a(
                            rx.el.button(
                                "Dashboard",
                                class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
                                variant="ghost",
                            ),
                            href="/costs",
                        ),
                        rx.el.a(
                            rx.el.button(
                                "All Costs",
                                class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
                                variant="ghost",
                            ),
                            href="/all-costs",
                        ),
                        rx.el.a(
                            rx.el.button(
                                "Profile",
                                class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
                                variant="ghost",
                            ),
                            href="/profile",
                        ),
                        rx.el.button(
                            "Log Out",
                            on_click=MyAuthState.on_logout,
                            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
                            variant="ghost",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    rx.el.div(
                        rx.el.a(
                            rx.el.button(
                                "Log In",
                                class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
                                variant="ghost",
                            ),
                            href="/login",
                        ),
                        rx.el.a(
                            rx.el.button(
                                "Sign Up",
                                class_name="bg-violet-600 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-violet-700 transition-colors shadow-sm",
                            ),
                            href="/register",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                )
            ),
            class_name="flex items-center justify-between container mx-auto px-4",
        ),
        class_name="py-4 border-b border-gray-200 bg-white/80 backdrop-blur-sm sticky top-0 z-50",
    )


def main_layout(child: rx.Component) -> rx.Component:
    """The main layout for the app."""
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(child, class_name="container mx-auto px-4 py-8"),
            class_name="py-8",
        ),
        class_name="min-h-screen bg-gray-50 font-['Poppins']",
    )