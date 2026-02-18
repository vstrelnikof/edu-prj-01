from utils.state import AppState
from asciimatics.widgets import Frame, Layout, MultiColumnListBox, Button, Divider, Text, PopUpDialog
from asciimatics.exceptions import NextScene
from cli.tui.scene_type import SceneType

class ContactListView(Frame):
    def __init__(self, screen, state: AppState):
        super().__init__(screen, screen.height, screen.width, 
                         has_border=True, title="🔍 Пошук та Управління Контактами")
        self._state = state
        self.set_theme("bright")

        # 1. Створюємо Layout для пошукового рядка
        search_layout = Layout([1, 10, 1])
        self.add_layout(search_layout)
        # on_change викликає метод filter_list при кожному символі
        self._search_box = Text("🔎 Пошук:", name="search", on_change=self._filter_list)
        search_layout.add_widget(self._search_box, 1)

        # 2. Layout для таблиці
        list_layout = Layout([1], fill_frame=True)
        self.add_layout(list_layout)
        
        self._list_box = MultiColumnListBox(
            screen.height - 8,
            ["<25%", "<20%", "<20%", "<20%", "<15%"],
            [], # Спочатку порожній, заповниться в _filter_list
            # header=["Ім'я", "📱 Телефон", "📧 Email", "🏠 Адреса", "🎂 Дата"],
            name="contact_list"
        )
        list_layout.add_widget(self._list_box)
        list_layout.add_widget(Divider())

        # 3. Layout для кнопок управління
        button_layout = Layout([1, 1, 1])
        self.add_layout(button_layout)
        button_layout.add_widget(Button("Назад", self._on_back), 0)
        button_layout.add_widget(Button("Видалити", self._on_delete), 2)
        
        self.fix()
        self._filter_list() # Первинне заповнення списку

    def _filter_list(self):
        """Фільтрація списку контактів на основі тексту в пошуку."""
        search_term = self._search_box.value.lower() if self._search_box.value else ""
        
        filtered_data = []
        for i, c in enumerate(self._state.address_book_manager.contacts):
            # Перевіряємо збіг по імені або телефону
            if search_term in c.name.lower() or search_term in c.phone:
                filtered_data.append(([c.name, c.phone, c.email, c.address, c.birthday], i))
        
        self._list_box.options = filtered_data

    def _on_back(self):
        raise NextScene(SceneType.MAIN)

    def _on_delete(self):
        if self._list_box.value is not None:
            # Створюємо діалог підтвердження
            self.add_effect(
                PopUpDialog(
                    self._screen, 
                    "Ви впевнені, що хочете видалити цей контакт?", 
                    ["Так", "Ні"],
                    on_close=self._confirm_delete
                )
            )

    def _confirm_delete(self, selected_button_idx):
        # selected_button_idx == 0 відповідає кнопці "Так"
        if selected_button_idx == 0:
            idx = self._list_box.value

            if (idx is None):
                raise ValueError("selected_button_idx is None")

            self._state.address_book_manager.contacts.pop(idx)
            self._state.address_book_manager.save()
            self._filter_list() # Оновлюємо таблицю