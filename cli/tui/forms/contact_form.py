import logging
from utils.state import AppState
from asciimatics.widgets import Layout, Text, PopUpDialog, Label, Divider
from cli.tui.forms.base_form import BaseForm
from cli.tui.scene_type import SceneType
from managers.scene_manager import SceneManager
from utils.validator import Validator

class ContactForm(BaseForm):
    def __init__(self, screen, state: AppState):
        super().__init__(screen, state, can_scroll=False, title="👤 Новий контакт")
        self.required_fields = ["name"]
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        layout.add_widget(Label("Формат телефону: +380XXXXXXXXX"))
        layout.add_widget(Label("Формат дати:     YYYY-MM-DD"))

        layout.add_widget(Divider(draw_line=False))

        layout.add_widget(Text("Ім'я:", "name"))
        layout.add_widget(Text("Телефон:", "phone", validator=lambda phone_string:
                               Validator.validate_phone(phone_string, throw=False)
                               if phone_string else True))
        layout.add_widget(Text("Email:", "email", validator=lambda email_string:
                               Validator.validate_email(email_string, throw=False)
                               if email_string else True))
        layout.add_widget(Text("Адреса:", "address"))
        layout.add_widget(Text("День народження:", "birthday", validator=lambda date_string:
                               Validator.validate_date(date_string, throw=False)
                               if date_string else True))

        self.complete()

    def _ok(self):
        super()._ok()

        if not self.data or not self.validate_form(): return
        
        try:
            self._state.address_book_manager.add_contact_from_dict(self.data)
            self.add_effect(PopUpDialog(self._screen, "✅ Контакт успішно збережено!", ["Чудово"], 
                            on_close=lambda _: SceneManager.next(SceneType.MAIN))
            )
        except ValueError as e:
            logging.error(e)
            self.add_effect(
                PopUpDialog(self._screen, f"❌ Помилка: {str(e)}", ["Спробувати ще раз"])
            )
