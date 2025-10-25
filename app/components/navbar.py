import reflex as rx
from app.states.auth_state import MyAuthState
from app.states.ui_state import UIState
from app.states.notification_state import NotificationState
from app.models import Notification


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
                rx.cond(MyAuthState.is_authenticated, authenticated_nav(), guest_nav()),
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
        rx.cond(
            MyAuthState.current_user.email != "acf@admin.com",
            rx.el.a(
                "Erstelle Kosten",
                href="/costs",
                class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
            ),
        ),
        rx.el.a(
            "Alle Kosten",
            href="/all-costs",
            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
        ),
        rx.el.a(
            "Quick Entry",
            href="/quick-entry",
            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
        ),
        rx.el.a(
            "Profil",
            href="/profile",
            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
        ),
        notification_bell(),
        rx.el.button(
            "Abmelden",
            on_click=MyAuthState.on_logout,
            class_name="text-sm font-medium text-gray-600 hover:text-violet-600 transition-colors",
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
                rx.cond(
                    MyAuthState.current_user.email != "acf@admin.com",
                    rx.el.a(
                        "Erstelle Kosten",
                        href="/costs",
                        class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                        on_click=UIState.close_mobile_menu,
                    ),
                ),
                rx.el.a(
                    "Alle Kosten",
                    href="/all-costs",
                    class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                    on_click=UIState.close_mobile_menu,
                ),
                rx.el.a(
                    "Quick Entry",
                    href="/quick-entry",
                    class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                    on_click=UIState.close_mobile_menu,
                ),
                rx.el.a(
                    "Profil",
                    href="/profile",
                    class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                    on_click=UIState.close_mobile_menu,
                ),
                rx.el.a(
                    "Benachrichtigungen",
                    on_click=NotificationState.toggle_notifications,
                    class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                ),
                rx.el.button(
                    "Abmelden",
                    on_click=MyAuthState.on_logout,
                    class_name="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-50",
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
                    "Registrieren",
                    href="/register",
                    class_name="block px-4 py-2 text-gray-700 hover:bg-gray-50",
                    on_click=UIState.close_mobile_menu,
                ),
                class_name="space-y-1 py-2",
            ),
        ),
        class_name="md:hidden border-t border-gray-200 bg-white shadow-sm",
    )


def notification_bell() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("bell", size=20),
            rx.cond(
                NotificationState.unread_count > 0,
                rx.el.span(
                    NotificationState.unread_count.to_string(),
                    class_name="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-xs text-white",
                ),
            ),
            on_click=[
                NotificationState.toggle_notifications,
                NotificationState.load_notifications,
            ],
            class_name="relative rounded-full p-2 text-gray-600 hover:text-violet-600 focus:outline-none",
        ),
        rx.cond(NotificationState.show_notifications, notification_dropdown()),
        class_name="relative",
    )


def notification_dropdown() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Benachrichtigungen", class_name="font-semibold"),
            rx.el.button(
                "Alle als gelesen markieren",
                on_click=NotificationState.mark_all_as_read,
                class_name="text-xs text-violet-600 hover:underline",
            ),
            class_name="flex justify-between items-center px-4 py-2 border-b",
        ),
        rx.el.div(
            rx.cond(
                NotificationState.notifications.length() > 0,
                rx.foreach(NotificationState.notifications, notification_item),
                rx.el.p(
                    "Keine neuen Benachrichtigungen",
                    class_name="p-4 text-sm text-gray-500",
                ),
            ),
            class_name="max-h-80 overflow-y-auto divide-y",
        ),
        class_name="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border z-50",
    )


def notification_item(notification: Notification) -> rx.Component:
    return rx.el.div(
        rx.el.p(notification.message, class_name="text-sm"),
        rx.el.p(
            rx.moment(notification.created_at, "fromNow"),
            class_name="text-xs text-gray-500 mt-1",
        ),
        class_name=rx.cond(
            notification.is_read,
            "p-4 hover:bg-gray-50",
            "p-4 bg-violet-50 hover:bg-violet-100",
        ),
        on_click=NotificationState.mark_as_read(notification.id),
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
        on_mount=NotificationState.load_notifications,
    )