import reflex as rx
from app.components.navbar import main_layout
from app.states.auth_state import MyAuthState
from app.states.quick_entry_state import QuickEntryState
from app.models import Member
from app.pages.quick_entry import login_prompt


def tile_entry_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.cond(MyAuthState.is_authenticated, tile_entry_view(), login_prompt()),
            on_mount=QuickEntryState.get_all_members,
        )
    )


def tile_entry_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Tile Cost Entry",
                class_name="text-xl md:text-3xl font-bold text-gray-900",
            ),
            class_name="flex justify-between items-center mb-2 md:mb-4",
        ),
        rx.el.input(
            placeholder="Search members by name...",
            on_change=QuickEntryState.set_search_query.debounce(300),
            class_name="w-full max-w-sm px-3 py-2 md:px-4 md:py-3 mb-2 md:mb-4 border border-gray-300 rounded-lg md:rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-violet-500 text-sm md:text-base",
        ),
        rx.el.div(
            rx.foreach(QuickEntryState.filtered_members, member_tile),
            class_name="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 md:gap-4",
        ),
        selection_dialog(),
        confirmation_dialog(),
    )


def member_tile(member: Member) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={member.name}",
                class_name="w-12 h-12 md:w-16 md:h-16 rounded-full mb-1 md:mb-2 bg-violet-100 shadow-sm",
            ),
            rx.el.h3(
                member.name,
                class_name="font-semibold text-gray-800 text-center truncate w-full px-1 md:px-2 text-xs md:text-base",
            ),
            class_name="flex flex-col items-center justify-center h-full w-full",
        ),
        on_click=lambda: QuickEntryState.open_selection(member.id),
        class_name="bg-white rounded-xl md:rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg transition-all transform hover:scale-[1.02] active:scale-95 p-2 md:p-4 h-28 md:h-48 w-full flex flex-col items-center justify-center",
    )


def selection_dialog() -> rx.Component:
    member_id = QuickEntryState.selected_member_id
    form_state = QuickEntryState.get_form_state[member_id]
    is_custom_category = form_state["category"] == "Anderes"
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-md z-50 animate-in fade-in duration-200"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        QuickEntryState.selected_member.name,
                        class_name="text-3xl font-bold text-gray-900 text-center mb-2",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Wähle eine Option oder erstelle einen benutzerdefinierten Eintrag.",
                        class_name="text-gray-500 text-center mb-8",
                    ),
                    rx.cond(
                        ~QuickEntryState.is_custom_form_visible,
                        rx.el.div(
                            rx.el.button(
                                rx.el.div(
                                    rx.icon("cup-soda", size=48, class_name="mb-2"),
                                    rx.el.span(
                                        "Nicht-alkoholisch",
                                        class_name="text-xl font-semibold",
                                    ),
                                    rx.el.span(
                                        "€1.50", class_name="text-lg opacity-80"
                                    ),
                                    class_name="flex flex-col items-center",
                                ),
                                on_click=lambda: QuickEntryState.add_quick_drink_for_member(
                                    member_id, "non-alcoholic"
                                ),
                                class_name="bg-blue-500 hover:bg-blue-600 text-white rounded-2xl p-8 shadow-lg transition-transform active:scale-95 flex justify-center items-center h-48",
                            ),
                            rx.el.button(
                                rx.el.div(
                                    rx.icon("beer", size=48, class_name="mb-2"),
                                    rx.el.span(
                                        "Alkoholisch",
                                        class_name="text-xl font-semibold",
                                    ),
                                    rx.el.span(
                                        "€2.50", class_name="text-lg opacity-80"
                                    ),
                                    class_name="flex flex-col items-center",
                                ),
                                on_click=lambda: QuickEntryState.add_quick_drink_for_member(
                                    member_id, "alcoholic"
                                ),
                                class_name="bg-amber-500 hover:bg-amber-600 text-white rounded-2xl p-8 shadow-lg transition-transform active:scale-95 flex justify-center items-center h-48",
                            ),
                            rx.el.button(
                                rx.el.div(
                                    rx.icon("pencil", size=32, class_name="mb-2"),
                                    rx.el.span(
                                        "Anderes / Manuell",
                                        class_name="text-lg font-medium",
                                    ),
                                    class_name="flex flex-col items-center",
                                ),
                                on_click=QuickEntryState.toggle_custom_form,
                                class_name="bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-2xl p-6 shadow-sm transition-colors md:col-span-2 h-24 flex justify-center items-center border-2 border-dashed border-gray-300",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Kategorie",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.select(
                                    rx.el.option(
                                        "Bitte wählen...", value="", disabled=True
                                    ),
                                    rx.foreach(
                                        QuickEntryState.categories.keys(),
                                        lambda c: rx.el.option(c, value=c),
                                    ),
                                    value=form_state["category"],
                                    on_change=lambda value: QuickEntryState.set_form_field(
                                        member_id, "category", value
                                    ),
                                    class_name="w-full p-4 bg-gray-50 border border-gray-300 rounded-xl text-lg focus:ring-2 focus:ring-violet-500",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Betrag (€)",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    type="number",
                                    placeholder="0.00",
                                    on_change=lambda value: QuickEntryState.set_form_field(
                                        member_id, "amount", value
                                    ),
                                    is_disabled=~is_custom_category
                                    & (form_state["category"] != ""),
                                    class_name="w-full p-4 bg-gray-50 border border-gray-300 rounded-xl text-lg focus:ring-2 focus:ring-violet-500 disabled:bg-gray-100",
                                    default_value=form_state["amount"],
                                    custom_attrs={
                                        "inputmode": "decimal",
                                        "pattern": "[0-9]*",
                                    },
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Beschreibung (Optional)",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    type="text",
                                    placeholder="z.B. Pizza, Taxi...",
                                    on_change=lambda value: QuickEntryState.set_form_field(
                                        member_id, "description", value
                                    ),
                                    class_name="w-full p-4 bg-gray-50 border border-gray-300 rounded-xl text-lg focus:ring-2 focus:ring-violet-500",
                                    default_value=form_state["description"],
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    "Hinzufügen",
                                    on_click=lambda: QuickEntryState.add_cost_for_member(
                                        member_id
                                    ),
                                    class_name="flex-1 bg-violet-600 text-white p-4 rounded-xl text-lg font-semibold hover:bg-violet-700 shadow-md",
                                ),
                                rx.el.button(
                                    "Zurück",
                                    on_click=QuickEntryState.toggle_custom_form,
                                    class_name="flex-none bg-gray-200 text-gray-800 p-4 rounded-xl text-lg font-medium hover:bg-gray-300",
                                ),
                                class_name="flex gap-3",
                            ),
                            class_name="bg-white p-1 rounded-lg animate-in slide-in-from-right duration-200",
                        ),
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Abbrechen",
                                class_name="w-full py-4 text-gray-500 hover:text-gray-800 font-medium transition-colors",
                            )
                        ),
                        class_name="mt-6 border-t pt-2",
                    ),
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-3xl shadow-2xl p-8 w-[95vw] max-w-2xl max-h-[90vh] overflow-y-auto z-50 focus:outline-none animate-in zoom-in-95 duration-200",
            ),
        ),
        open=QuickEntryState.is_selection_open,
        on_open_change=QuickEntryState.set_is_selection_open,
    )


def confirmation_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-violet-900/40 backdrop-blur-md z-[60] animate-in fade-in duration-300"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.icon("check", size=80, class_name="text-white"),
                        class_name="w-32 h-32 rounded-full bg-green-500 flex items-center justify-center mb-6 shadow-lg animate-in zoom-in duration-300",
                    ),
                    rx.radix.primitives.dialog.title(
                        "Erfolgreich gebucht!",
                        class_name="text-3xl font-bold text-gray-900 text-center mb-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            QuickEntryState.confirmation_details["member_name"],
                            class_name="text-xl font-semibold text-gray-800",
                        ),
                        rx.el.p(
                            QuickEntryState.confirmation_details["item_name"],
                            class_name="text-lg text-gray-600 mt-1",
                        ),
                        rx.el.p(
                            QuickEntryState.confirmation_details["amount"],
                            class_name="text-4xl font-bold text-violet-600 mt-4",
                        ),
                        class_name="text-center my-6 bg-gray-50 p-6 rounded-2xl w-full",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Rückgängig",
                            on_click=QuickEntryState.undo_last_booking,
                            class_name="flex-none bg-red-100 text-red-600 text-base font-medium px-6 py-3 rounded-2xl hover:bg-red-200 hover:text-red-700 shadow-sm transition-colors active:scale-95",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "OK, Weiter",
                                on_click=QuickEntryState.close_confirmation,
                                class_name="flex-1 bg-violet-600 text-white text-xl font-bold py-5 rounded-2xl hover:bg-violet-700 shadow-lg transition-transform active:scale-95",
                            )
                        ),
                        class_name="flex items-center gap-4 w-full mt-2",
                    ),
                    class_name="flex flex-col items-center",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-3xl shadow-2xl p-10 w-[90vw] max-w-md z-[60] focus:outline-none animate-in zoom-in-95 duration-200",
            ),
        ),
        open=QuickEntryState.show_confirmation,
        on_open_change=QuickEntryState.set_show_confirmation,
    )