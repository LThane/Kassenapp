import reflex as rx


class UIState(rx.State):
    mobile_menu_open: bool = False

    @rx.event
    def toggle_mobile_menu(self):
        self.mobile_menu_open = not self.mobile_menu_open

    @rx.event
    def close_mobile_menu(self):
        self.mobile_menu_open = False
