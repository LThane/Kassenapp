import reflex as rx
from app.states.auth_state import MyAuthState
from app.states.ui_state import UIState


def navbar() -> rx.Component:
    """A responsive navbar with user authentication status."""
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon("layers", size=24, class_name="text-violet-600"),
                    rx.el.span(
                        "Kassen-App", class_name="font-bold text-lg text-gray-800"
                    ),
                    class_name="flex items-center gap-2",
                ),
                href="/",
            ),
            # Desktop navigation
            rx.el.div(
                rx.cond(
                    MyAuthState.is_authenticated,
                    rx.el.div(
                        rx.el.a(
                            rx.el.button(
                                "Erstelle Kosten",
                                class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
                                variant="ghost",
                            ),
                            href="/costs",
                        ),
                        rx.el.a(
                            rx.el.button(
                                "Alle Kosten",
                                class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
                                variant="ghost",
                            ),
                            href="/all-costs",
                        ),
                        rx.el.a(
                            rx.el.button(
                                "Profil",
                                class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
                                variant="ghost",
                            ),
                            href="/profile",
                        ),
                        rx.el.button(
                            "Abmelden",
                            on_click=MyAuthState.on_logout,
                            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
                            variant="ghost",
                        ),
                        class_name="hidden md:flex items-center gap-4",
                    ),
                    rx.el.div(
                        rx.el.a(
                            rx.el.button(
                                "Anmelden",
                                class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
                                variant="ghost",
                            ),
                            href="/login",
                        ),
                        rx.el.a(
                            rx.el.button(
                                "Registrieren",
                                class_name="bg-violet-600 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-violet-700 transition-colors shadow-sm",
                            ),
                            href="/register",
                        ),
                        class_name="hidden md:flex items-center gap-2",
                    ),
                )
            ),
            # Mobile hamburger button
            rx.el.button(
                rx.icon("menu", size=22),
                on_click=UIState.toggle_mobile_menu,
                class_name="md:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-600 hover:text-violet-600 focus:outline-none",
                variant="ghost",
            ),
            class_name="flex items-center justify-between container mx-auto px-4",
        ),
        # Mobile menu panel
        rx.cond(
            UIState.mobile_menu_open,
            rx.el.div(
                rx.cond(
                    MyAuthState.is_authenticated,
                    rx.el.div(
                        rx.el.a("Erstelle Kosten", href="/costs", class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50", on_click=UIState.close_mobile_menu),
                        rx.el.a("Alle Kosten", href="/all-costs", class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50", on_click=UIState.close_mobile_menu),
                        rx.el.a("Profil", href="/profile", class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50", on_click=UIState.close_mobile_menu),
                        rx.el.button("Abmelden", on_click=MyAuthState.on_logout, class_name="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-50", variant="ghost"),
                        class_name="space-y-1",
                    ),
                    rx.el.div(
                        rx.el.a("Anmelden", href="/login", class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50", on_click=UIState.close_mobile_menu),
                        rx.el.a("Registrieren", href="/register", class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50", on_click=UIState.close_mobile_menu),
                        class_name="space-y-1",
                    ),
                ),
                class_name="md:hidden border-t border-gray-200 bg-white shadow-sm",
            ),
            rx.el.div(),
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