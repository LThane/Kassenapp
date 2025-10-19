import reflex as rx
from app.components.navbar import main_layout
from app.states.auth_state import MyAuthState
from app.states.all_costs_state import AllCostsState
from app.models import CostWithMember


def all_costs_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.cond(
                MyAuthState.is_authenticated,
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Alle Vereinskosten",
                            class_name="text-3xl font-bold text-gray-900",
                        ),
                        class_name="flex justify-between items-center mb-8",
                    ),
                    summary_cards(),
                    rx.el.div(all_costs_table(), class_name="mt-8"),
                    on_mount=AllCostsState.get_all_costs,
                ),
                rx.el.div(
                    rx.el.h1(
                        "Bitte melde dich an, um diese Seite zu sehen.",
                        class_name="text-2xl font-bold text-gray-800",
                    ),
                    rx.el.a(
                        "Zum Login",
                        href="/login",
                        class_name="text-violet-600 hover:underline mt-2",
                    ),
                    class_name="text-center p-8",
                ),
            )
        )
    )


def summary_cards() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Gesamtausgaben (alle)", class_name="text-sm font-medium text-gray-500"
            ),
                rx.el.p(
                    "€" + AllCostsState.total_spent_all.to_string(),
                class_name="mt-1 text-3xl font-semibold text-gray-900",
            ),
            class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
        rx.el.div(
            rx.el.h3(
                "Anzahl Kosten (alle)", class_name="text-sm font-medium text-gray-500"
            ),
            rx.el.p(
                AllCostsState.total_costs_all,
                class_name="mt-1 text-3xl font-semibold text-gray-900",
            ),
            class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
        rx.el.div(
            rx.el.h3(
                "Durchschn. Kosten (alle)", class_name="text-sm font-medium text-gray-500"
            ),
                rx.el.p(
                    "€" + AllCostsState.average_cost_all.to_string(),
                class_name="mt-1 text-3xl font-semibold text-gray-900",
            ),
            class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
        rx.el.div(
            rx.el.h3("Aktive Mitglieder", class_name="text-sm font-medium text-gray-500"),
            rx.el.p(
                AllCostsState.total_members,
                class_name="mt-1 text-3xl font-semibold text-gray-900",
            ),
            class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
        class_name="grid md:grid-cols-4 gap-6",
    )


def all_costs_table() -> rx.Component:
    return rx.el.div(
        rx.foreach(AllCostsState.costs_by_week_and_member, weekly_cost_section),
        class_name="space-y-8",
    )


def weekly_cost_section(week_data: list) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                f"Woche ab {week_data[0]}", class_name="text-xl font-bold text-gray-800"
            ),
            rx.el.p(
                 f"Total: €{week_data[2]:.2f}",
                class_name="text-lg font-semibold text-violet-600",
            ),
            class_name="flex justify-between items-center p-4 bg-gray-100 rounded-t-lg",
        ),
        rx.el.div(
            rx.foreach(week_data[1], member_cost_section),
            class_name="bg-white rounded-b-lg border border-gray-200 shadow-sm divide-y divide-gray-200",
        ),
    )


def member_cost_section(member_data: list) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(member_data[0], class_name="font-semibold text-gray-700"),
            rx.el.p(
                 f"Subtotal: €{member_data[2]:.2f}",
                class_name="font-semibold text-gray-600",
            ),
            class_name="flex justify-between items-center p-3 bg-gray-50",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                                    "Beschreibung",
                            class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600 w-2/5",
                        ),
                        rx.el.th(
                                    "Betrag",
                            class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600 w-1/5",
                        ),
                        rx.el.th(
                                    "Datum",
                            class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600 w-1/5",
                        ),
                        rx.el.th(
                                    "Kategorie",
                            class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600 w-1/5",
                        ),
                    )
                ),
                rx.el.tbody(rx.foreach(member_data[1], all_cost_row)),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-x-auto",
        ),
    )


def all_cost_row(cost: CostWithMember) -> rx.Component:
    return rx.el.tr(
        rx.el.td(cost["description"], class_name="px-4 py-3 text-sm text-gray-800"),
        rx.el.td(
              "€" + cost["amount"].to_string(),
            class_name="px-4 py-3 text-sm text-gray-800",
        ),
        rx.el.td(cost["date"], class_name="px-4 py-3 text-sm text-gray-800"),
        rx.el.td(cost["category"], class_name="px-4 py-3 text-sm text-gray-800"),
        class_name="hover:bg-gray-50",
    )