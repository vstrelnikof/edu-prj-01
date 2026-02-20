import logging
from models.contact import Contact
from utils.state import AppState
from utils.validator import Validator
from asciimatics.screen import Screen
from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, PopUpDialog, Label, Divider
from cli.tui.forms.base_form import BaseForm
from cli.tui.scene_type import SceneType
from factories.scene_factory import SceneFactory

class ContactForm(BaseForm):
    _esc_key_path: str = SceneType.CONTACTS_LIST

    def __init__(self, screen: Screen, state: AppState):
        super().__init__(screen, state, can_scroll=False)
    
    def _render_content(self) -> None:
        self._required_fields = ["name"]
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        layout.add_widget(Label("Формат телефону: +380XXXXXXXXX"))
        layout.add_widget(Label("Формат дати:     YYYY-MM-DD"))

        layout.add_widget(Divider())

        layout.add_widget(Text("Ім'я*:", "name"))
        layout.add_widget(Text("Телефон:", "phone", validator=lambda phone_string:
                               not phone_string or Validator.validate_phone(phone_string)))
        layout.add_widget(Text("Email:", "email", validator=lambda email_string:
                               not email_string or Validator.validate_email(email_string)))
        layout.add_widget(Text("Адреса:", "address"))
        layout.add_widget(Text("День народження:", "birthday", validator=lambda date_string:
                               not date_string or Validator.validate_date(date_string)))

        layout.add_widget(Divider())
    
    def reset(self) -> None:
        super().reset()
        self.title = "👤 Новий контакт" if self._state.edit_index is None else "👤 Редагування контакту"
        if self._edit_index is not None:
            contact: Contact = self._state.address_book_manager.contacts[self._edit_index]
            self.data = {
                "name": contact.name,
                "phone": contact.phone,
                "email": contact.email,
                "address": contact.address,
                "birthday": contact.birthday
            }
        else:
            self.data = {
                "name": "", "phone": "", "email": "", "address": "", "birthday": ""
            }
    
    def _handle_saved(self):
        super().reset()
        SceneFactory.next(SceneType.CONTACTS_LIST)

    def _ok(self):
        assert self.scene is not None
        self.save()

        if not self.data or not self._validate_form():
            return

        try:
            if self._edit_index is None:
                self._state.address_book_manager.add_contact(self.data)
            else:
                self._state.address_book_manager.edit_contact(self._edit_index, self.data)
            self.scene.add_effect(PopUpDialog(self._screen,
                                              f"✅ Контакт \"{self.data["name"]}\" успішно збережено!",
                                              ["Чудово"], 
                                              on_close=lambda _: self._handle_saved())
            )
            self._clear_edit()
        except ValueError as e:
            logging.error(e)
            self.scene.add_effect(
                PopUpDialog(self._screen, f"❌ Помилка: {str(e)}", ["Спробувати ще раз"])
            )
    
    def _cancel(self) -> None:
        self._clear_edit()
        SceneFactory.next(SceneType.CONTACTS_LIST)

