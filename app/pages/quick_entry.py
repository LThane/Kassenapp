import reflex as rx
from app.components.navbar import main_layout
from app.states.auth_state import MyAuthState
from app.states.quick_entry_state import QuickEntryState
from app.models import Member


def quick_entry_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.cond(MyAuthState.is_authenticated, quick_entry_view(), login_prompt()),
            on_mount=QuickEntryState.get_all_members,
        )
    )


def login_prompt() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Bitte anmelden", class_name="text-2xl font-bold text-gray-800"),
        rx.el.p(
            "Du musst angemeldet sein, um diese Funktion zu nutzen.",
            class_name="text-gray-600",
        ),
        rx.el.a(
            "Zum Login",
            href="/login",
            class_name="text-violet-600 hover:underline mt-4 inline-block",
        ),
        class_name="text-center p-8 bg-white rounded-xl shadow-sm",
    )


def quick_entry_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Quick Cost Entry", class_name="text-3xl font-bold text-gray-900"),
            class_name="flex justify-between items-center mb-8",
        ),
        rx.el.div(
            rx.foreach(QuickEntryState.members, member_entry_row),
            class_name="space-y-4",
        ),
    )


def member_entry_row(member: Member) -> rx.Component:
    form_state = QuickEntryState.get_form_state[member.id]
    is_custom_category = form_state["category"] == "Anderes"
    return rx.el.div(
        rx.el.h3(member.name, class_name="text-lg font-semibold text-gray-800 mb-2"),
        rx.el.div(
            rx.el.select(
                rx.el.option("Select Category", value="", disabled=True),
                rx.foreach(
                    QuickEntryState.categories.keys(),
                    lambda c: rx.el.option(c, value=c),
                ),
                value=form_state["category"],
                on_change=lambda value: QuickEntryState.set_form_field(
                    member.id, "category", value
                ),
                class_name="flex-1 min-w-[150px] px-3 py-2 bg-white border border-gray-300 rounded-md text-sm text-gray-800 shadow-sm focus:outline-none focus:ring-violet-500 focus:border-violet-500",
            ),
            rx.el.input(
                placeholder="Amount",
                on_change=lambda value: QuickEntryState.set_form_field(
                    member.id, "amount", value
                ),
                is_disabled=~is_custom_category & (form_state["category"] != ""),
                type="number",
                class_name="flex-1 min-w-[100px] px-3 py-2 bg-white border border-gray-300 rounded-md text-sm text-gray-800 shadow-sm placeholder-gray-400 focus:outline-none focus:ring-violet-500 focus:border-violet-500 disabled:bg-gray-100",
                default_value=form_state["amount"],
            ),
            rx.el.input(
                placeholder="Description (optional)",
                on_change=lambda value: QuickEntryState.set_form_field(
                    member.id, "description", value
                ),
                class_name="flex-1 min-w-[150px] px-3 py-2 bg-white border border-gray-300 rounded-md text-sm text-gray-800 shadow-sm placeholder-gray-400 focus:outline-none focus:ring-violet-500 focus:border-violet-500",
                default_value=form_state["description"],
            ),
            rx.el.input(
                type="date",
                on_change=lambda value: QuickEntryState.set_form_field(
                    member.id, "date", value
                ),
                class_name="flex-1 min-w-[130px] px-3 py-2 bg-white border border-gray-300 rounded-md text-sm text-gray-800 shadow-sm focus:outline-none focus:ring-violet-500 focus:border-violet-500",
                default_value=form_state["date"],
            ),
            rx.el.button(
                "Add",
                on_click=lambda: QuickEntryState.add_cost_for_member(member.id),
                class_name="bg-violet-600 text-white px-4 py-2 rounded-md hover:bg-violet-700 transition-colors shadow-sm",
            ),
            rx.el.button(
                rx.icon("cup-soda", size=20),
                on_click=lambda: QuickEntryState.add_quick_drink_for_member(
                    member.id, "non-alcoholic"
                ),
                class_name="bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 transition-colors shadow-sm",
            ),
            rx.el.button(
                rx.icon("beer", size=20),
                on_click=lambda: QuickEntryState.add_quick_drink_for_member(
                    member.id, "alcoholic"
                ),
                class_name="bg-yellow-500 text-white p-2 rounded-md hover:bg-yellow-600 transition-colors shadow-sm",
            ),
            class_name="flex flex-wrap items-center gap-2",
        ),
        class_name="p-4 bg-white rounded-xl border border-gray-200 shadow-sm",
    )