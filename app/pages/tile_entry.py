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
            rx.el.h1("Tile Cost Entry", class_name="text-3xl font-bold text-gray-900"),
            class_name="flex justify-between items-center mb-8",
        ),
        rx.el.input(
            placeholder="Search members by name...",
            on_change=QuickEntryState.set_search_query.debounce(300),
            class_name="w-full max-w-sm px-4 py-2 mb-8 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-violet-500",
        ),
        rx.el.div(
            rx.foreach(QuickEntryState.filtered_members, member_tile),
            class_name="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4",
        ),
    )


def member_tile(member: Member) -> rx.Component:
    is_form_open = QuickEntryState.open_forms.contains(member.id)
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.menu.root(
                    rx.menu.trigger(
                        rx.el.button(
                            rx.icon(
                                "ellipsis-vertical",
                                size=20,
                                class_name="text-gray-500 hover:text-violet-600",
                            ),
                            class_name="p-1 rounded-full hover:bg-gray-100 focus:outline-none",
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            "Non-alcoholic (€1.50)",
                            on_click=lambda: QuickEntryState.add_quick_drink_for_member(
                                member.id, "non-alcoholic"
                            ),
                            class_name="cursor-pointer",
                        ),
                        rx.menu.item(
                            "Alcoholic (€2.50)",
                            on_click=lambda: QuickEntryState.add_quick_drink_for_member(
                                member.id, "alcoholic"
                            ),
                            class_name="cursor-pointer",
                        ),
                        rx.menu.separator(),
                        rx.menu.item(
                            "Add Custom Cost...",
                            on_click=lambda: QuickEntryState.toggle_form(member.id),
                            class_name="cursor-pointer font-medium text-violet-600",
                        ),
                        class_name="bg-white rounded-lg shadow-lg border border-gray-100 min-w-[200px] overflow-hidden z-50",
                    ),
                ),
                class_name="absolute top-2 right-2",
            ),
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={member.name}",
                    class_name="w-16 h-16 rounded-full mb-3 bg-violet-100",
                ),
                rx.el.h3(
                    member.name,
                    class_name="font-semibold text-gray-800 text-center truncate w-full px-2 text-sm",
                ),
                class_name="flex flex-col items-center mt-4",
            ),
            rx.cond(is_form_open, tile_inline_form(member)),
            class_name="p-4 h-full flex flex-col",
        ),
        class_name="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all relative overflow-hidden",
    )


def tile_inline_form(member: Member) -> rx.Component:
    form_state = QuickEntryState.get_form_state[member.id]
    is_custom_category = form_state["category"] == "Anderes"
    return rx.el.div(
        rx.el.div(
            rx.el.select(
                rx.el.option("Category...", value="", disabled=True),
                rx.foreach(
                    QuickEntryState.categories.keys(),
                    lambda c: rx.el.option(c, value=c),
                ),
                value=form_state["category"],
                on_change=lambda value: QuickEntryState.set_form_field(
                    member.id, "category", value
                ),
                class_name="w-full px-2 py-1.5 text-xs bg-gray-50 border border-gray-300 rounded focus:outline-none focus:border-violet-500",
            ),
            class_name="mb-2",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Amount",
                on_change=lambda value: QuickEntryState.set_form_field(
                    member.id, "amount", value
                ),
                is_disabled=~is_custom_category & (form_state["category"] != ""),
                type="number",
                class_name="w-full px-2 py-1.5 text-xs bg-gray-50 border border-gray-300 rounded focus:outline-none focus:border-violet-500 disabled:bg-gray-100",
                default_value=form_state["amount"],
            ),
            class_name="mb-2",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Desc (opt)",
                on_change=lambda value: QuickEntryState.set_form_field(
                    member.id, "description", value
                ),
                class_name="w-full px-2 py-1.5 text-xs bg-gray-50 border border-gray-300 rounded focus:outline-none focus:border-violet-500",
                default_value=form_state["description"],
            ),
            class_name="mb-2",
        ),
        rx.el.div(
            rx.el.input(
                type="date",
                on_change=lambda value: QuickEntryState.set_form_field(
                    member.id, "date", value
                ),
                class_name="w-full px-2 py-1.5 text-xs bg-gray-50 border border-gray-300 rounded focus:outline-none focus:border-violet-500",
                default_value=form_state["date"],
            ),
            class_name="mb-2",
        ),
        rx.el.div(
            rx.el.button(
                "Add",
                on_click=lambda: QuickEntryState.add_cost_for_member(member.id),
                class_name="w-full bg-violet-600 text-white text-xs font-medium py-1.5 rounded hover:bg-violet-700 transition-colors",
            ),
            rx.el.button(
                "Cancel",
                on_click=lambda: QuickEntryState.toggle_form(member.id),
                class_name="w-full bg-gray-200 text-gray-700 text-xs font-medium py-1.5 rounded hover:bg-gray-300 transition-colors",
            ),
            class_name="grid grid-cols-2 gap-2",
        ),
        class_name="mt-4 pt-4 border-t border-gray-100 animate-in fade-in slide-in-from-top-2 duration-200",
    )