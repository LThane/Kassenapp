import reflex as rx
from app.states.auth_state import MyAuthState
from app.states.ui_state import UIState
from app.states.acf_state import ACFState
from app.states.acf_state import ACFState


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
            rx.el.div(
                rx.cond(
                    MyAuthState.is_authenticated,
                    authenticated_nav(),
                    rx.cond(ACFState.is_acf_authenticated, acf_nav(), guest_nav()),
                ),
                class_name="hidden md:flex items-center gap-4",
            ),
            rx.el.button(
                rx.icon("menu", size=22),
                on_click=UIState.toggle_mobile_menu,
                class_name="md:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-600 hover:text-violet-600 focus:outline-none",
                variant="ghost",
            ),
            class_name="flex items-center justify-between container mx-auto px-4",
        ),
        rx.cond(UIState.mobile_menu_open, mobile_menu(), rx.el.div()),
        class_name="py-4 border-b border-gray-200 bg-white/80 backdrop-blur-sm sticky top-0 z-50",
    )


def authenticated_nav() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            "Erstelle Kosten",
            href="/costs",
            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
        ),
        rx.el.a(
            "Alle Kosten",
            href="/all-costs",
            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
        ),
        rx.el.a(
            "Profil",
            href="/profile",
            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
        ),
        rx.el.button(
            "Abmelden",
            on_click=MyAuthState.on_logout,
            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
            variant="ghost",
        ),
        class_name="flex items-center gap-4",
    )


def acf_nav() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            "Quick Entry",
            href="/quick-entry",
            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
        ),
        rx.el.button(
            "ACF Logout",
            on_click=ACFState.acf_logout,
            class_name="text-sm font-medium text-red-500 hover:text-red-700 transition-colors",
            variant="ghost",
        ),
        class_name="flex items-center gap-4",
    )


def guest_nav() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            "Anmelden",
            href="/login",
            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
        ),
        rx.el.a(
            "ACF Login",
            href="/acf-login",
            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
        ),
        rx.el.a(
            rx.el.button(
                "Registrieren",
                class_name="bg-violet-600 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-violet-700 transition-colors shadow-sm",
            ),
            href="/register",
        ),
        class_name="flex items-center gap-2",
    )


def mobile_menu() -> rx.Component:
    return rx.el.div(
        rx.cond(
            MyAuthState.is_authenticated,
            rx.el.div(
                rx.el.a(
                    "Erstelle Kosten",
                    href="/costs",
                    class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                    on_click=UIState.close_mobile_menu,
                ),
                rx.el.a(
                    "Alle Kosten",
                    href="/all-costs",
                    class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                    on_click=UIState.close_mobile_menu,
                ),
                rx.el.a(
                    "Profil",
                    href="/profile",
                    class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                    on_click=UIState.close_mobile_menu,
                ),
                rx.el.button(
                    "Abmelden",
                    on_click=MyAuthState.on_logout,
                    class_name="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-50",
                    variant="ghost",
                ),
                class_name="space-y-1 py-2",
            ),
            rx.cond(
                ACFState.is_acf_authenticated,
                rx.el.div(
                    rx.el.a(
                        "Quick Entry",
                        href="/quick-entry",
                        class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                        on_click=UIState.close_mobile_menu,
                    ),
                    rx.el.button(
                        "ACF Logout",
                        on_click=ACFState.acf_logout,
                        class_name="w-full text-left px-4 py-2 text-red-500 hover:bg-gray-50",
                        variant="ghost",
                    ),
                    class_name="space-y-1 py-2",
                ),
                rx.el.div(
                    rx.el.a(
                        "Anmelden",
                        href="/login",
                        class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                        on_click=UIState.close_mobile_menu,
                    ),
                    rx.el.a(
                        "ACF Login",
                        href="/acf-login",
                        class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                        on_click=UIState.close_mobile_menu,
                    ),
                    rx.el.a(
                        "Registrieren",
                        href="/register",
                        class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                        on_click=UIState.close_mobile_menu,
                    ),
                    class_name="space-y-1 py-2",
                ),
            ),
        ),
        class_name="md:hidden border-t border-gray-200 bg-white shadow-sm",
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