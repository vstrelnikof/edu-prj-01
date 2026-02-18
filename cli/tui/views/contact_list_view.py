from utils.state import AppState
from asciimatics.screen import Screen
from asciimatics.widgets import Layout, MultiColumnListBox
from asciimatics.exceptions import NextScene
from cli.tui.views.base_view import BaseView
from cli.tui.scene_type import SceneType

class ContactListView(BaseView):
    def __init__(self, screen: Screen, state: AppState):
        super().__init__(screen, state, 
                         title="🔍 Пошук та Управління Контактами")
    
    def _render_content(self) -> None:
        list_layout = Layout([1], fill_frame=True)
        self.add_layout(list_layout)
        
        self._list_box = MultiColumnListBox(
            name="contact_list",
            height=self.screen.height - 5,
            columns=["<25%", "<20%", "<20%", "<20%", "<15%"],
            titles=["👤 Ім'я", "📱 Телефон", "📧 Email", "🏠 Адреса", "🎂 Дата"],
            options=[], # Спочатку порожній, заповниться в _filter_list
        )
        list_layout.add_widget(self._list_box)

    def _filter_list(self):
        """Фільтрація списку контактів на основі тексту в пошуку."""
        search_term = self._search_box.value.lower() if self._search_box.value else ""
        
        filtered_data = []
        for i, contact in enumerate(self._state.address_book_manager.contacts):
            for _, contact_field_value in vars(contact).items():
                if search_term in contact_field_value.lower():
                    filtered_data.append(([contact.name,
                                           contact.phone,
                                           contact.email,
                                           contact.address,
                                           contact.birthday], i))
                    break
        
        self._list_box.options = filtered_data
    
    def _on_create(self) -> None:
        super()._on_create()
        raise NextScene(SceneType.CONTACT_FORM)
    
    def _on_edit(self) -> None:
        super()._on_edit()
        raise NextScene(SceneType.CONTACT_FORM)

    def _confirm_delete(self, selected_button_idx):
        # selected_button_idx == 0 відповідає кнопці "Так"
        if selected_button_idx == 0:
            index = self._list_box.value

            if (index is None):
                raise ValueError("selected_button_idx is None")

            self._state.address_book_manager.delete_contact(index)
            self._filter_list() # Оновлюємо таблицю