import reflex as rx


def auth_layout(child: rx.Component) -> rx.Component:
    """A layout for the authentication pages."""
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.icon("layers", size=32, class_name="text-violet-600"),
                class_name="p-2 bg-violet-100 rounded-lg",
            ),
            child,
            class_name="w-full max-w-md p-8 space-y-6 bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 font-['Poppins']",
    )