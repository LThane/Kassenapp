import reflex as rx


class ACFState(rx.State):
    is_acf_authenticated: bool = False

    @rx.event
    def acf_login(self, form_data: dict):
        """Log the ACF user in."""
        if form_data.get("username") == "ACF" and form_data.get("password") == "123":
            self.is_acf_authenticated = True
            return rx.redirect("/quick-entry")
        else:
            return rx.toast.error("Invalid credentials.")

    @rx.event
    def acf_logout(self):
        """Log the ACF user out."""
        self.is_acf_authenticated = False
        return rx.redirect("/acf-login")