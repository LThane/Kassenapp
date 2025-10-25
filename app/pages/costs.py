import reflex as rx
from app.components.navbar import main_layout
from app.states.auth_state import MyAuthState
from app.states.cost_state import CostState


def costs_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.cond(
                MyAuthState.is_authenticated,
                rx.cond(
                    MyAuthState.current_user.email == "acf@admin.com",
                    rx.el.div(
                        rx.el.h1(
                            "Zugriff verweigert",
                            class_name="text-2xl font-bold text-gray-800",
                        ),
                        rx.el.p(
                            "Als ACF Admin nutze bitte die Quick Entry Seite, um Kosten für Mitglieder zu erfassen.",
                            class_name="mt-2 text-gray-600",
                        ),
                        rx.el.a(
                            "Zur Quick Entry Seite",
                            href="/quick-entry",
                            class_name="text-violet-600 hover:underline mt-4 inline-block",
                        ),
                        class_name="text-center p-8 bg-white rounded-xl shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h1(
                                "Meine Kostenübersicht",
                                class_name="text-3xl font-bold text-gray-900",
                            ),
                            class_name="flex justify-between items-center mb-8",
                        ),
                        summary_cards(),
                        rx.el.div(
                            quick_add_buttons(),
                            add_cost_form(),
                            costs_table(),
                            class_name="grid md:grid-cols-3 gap-8 mt-8",
                        ),
                        on_mount=CostState.get_costs,
                    ),
                ),
                rx.el.div(
                    rx.el.h1(
                        "Bitte melde dich an, um deine Kosten zu sehen.",
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
            rx.el.h3("Gesamtausgaben", class_name="text-sm font-medium text-gray-500"),
            rx.el.p(
                "€" + CostState.total_spent.to_string(),
                class_name="mt-1 text-3xl font-semibold text-gray-900",
            ),
            class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
        rx.el.div(
            rx.el.h3("Anzahl Kosten", class_name="text-sm font-medium text-gray-500"),
            rx.el.p(
                CostState.total_costs,
                class_name="mt-1 text-3xl font-semibold text-gray-900",
            ),
            class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
        rx.el.div(
            rx.el.h3(
                "Durchschnittliche Kosten",
                class_name="text-sm font-medium text-gray-500",
            ),
            rx.el.p(
                "€" + CostState.average_cost.to_string(),
                class_name="mt-1 text-3xl font-semibold text-gray-900",
            ),
            class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
        ),
        class_name="grid md:grid-cols-3 gap-6",
    )


def quick_add_buttons() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Quick Actions", class_name="text-xl font-semibold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.el.button(
                "Getränk (nicht-alkoholisch) - €1.50",
                on_click=lambda: CostState.add_quick_drink("non-alcoholic"),
                class_name="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500",
            ),
            rx.el.button(
                "Getränk (alkoholisch) - €2.50",
                on_click=lambda: CostState.add_quick_drink("alcoholic"),
                class_name="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500",
            ),
            class_name="space-y-3",
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm md:col-span-1 mb-8 md:mb-0",
    )


def add_cost_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Neue Ausgabe hinzufügen",
            class_name="text-xl font-semibold text-gray-800 mb-4",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Kategorie", class_name="block text-sm font-medium text-gray-700"
                ),
                rx.el.select(
                    rx.el.option("Kategorie auswählen", value="", disabled=True),
                    rx.foreach(
                        CostState.categories.keys(), lambda c: rx.el.option(c, value=c)
                    ),
                    id="category",
                    name="category",
                    required=True,
                    on_change=CostState.set_form_category,
                    value=CostState.form_category,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm text-gray-800 shadow-sm focus:outline-none focus:ring-violet-500 focus:border-violet-500",
                ),
                class_name="space-y-1",
            ),
            rx.cond(
                CostState.is_custom_category,
                rx.el.div(
                    rx.el.label(
                        "Betrag (€)",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        id="amount",
                        name="amount",
                        type="number",
                        required=True,
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm text-gray-800 shadow-sm placeholder-gray-400 focus:outline-none focus:ring-violet-500 focus:border-violet-500",
                        custom_attrs={"step": "0.01"},
                    ),
                    class_name="space-y-1",
                ),
                rx.el.div(),
            ),
            rx.el.div(
                rx.el.label(
                    "Beschreibung (optional)",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    id="description",
                    name="description",
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm text-gray-800 shadow-sm placeholder-gray-400 focus:outline-none focus:ring-violet-500 focus:border-violet-500",
                ),
                class_name="space-y-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Datum", class_name="block text-sm font-medium text-gray-700"
                ),
                rx.el.input(
                    id="date",
                    name="date",
                    type="date",
                    required=True,
                    default_value=CostState.today_date,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm text-gray-800 shadow-sm placeholder-gray-400 focus:outline-none focus:ring-violet-500 focus:border-violet-500",
                ),
                class_name="space-y-1",
            ),
            rx.el.button(
                "Ausgabe hinzufügen",
                type="submit",
                class_name="w-full mt-6 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-violet-600 hover:bg-violet-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500",
            ),
            on_submit=CostState.add_cost,
            reset_on_submit=True,
            class_name="space-y-4",
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm md:col-span-1",
    )


def costs_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Beschreibung",
                        class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                    ),
                    rx.el.th(
                        "Betrag",
                        class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                    ),
                    rx.el.th(
                        "Datum",
                        class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                    ),
                    rx.el.th(
                        "Kategorie",
                        class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                    ),
                    rx.el.th(
                        "Aktionen",
                        class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                    ),
                )
            ),
            rx.el.tbody(rx.foreach(CostState.costs, cost_row)),
            class_name="min-w-full divide-y divide-gray-200",
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm md:col-span-2 overflow-x-auto",
    )


def cost_row(cost: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(cost["description"], class_name="px-4 py-3 text-sm text-gray-800"),
        rx.el.td(
            "€" + cost["amount"].to_string(),
            class_name="px-4 py-3 text-sm text-gray-800",
        ),
        rx.el.td(cost["date"], class_name="px-4 py-3 text-sm text-gray-800"),
        rx.el.td(cost["category"], class_name="px-4 py-3 text-sm text-gray-800"),
        rx.el.td(
            rx.el.button(
                rx.icon("trash-2", size=16),
                on_click=lambda: CostState.delete_cost(cost["id"]),
                class_name="text-red-500 hover:text-red-700",
                variant="ghost",
            ),
            class_name="px-4 py-3 text-sm text-gray-800",
        ),
        class_name="hover:bg-gray-50",
    )