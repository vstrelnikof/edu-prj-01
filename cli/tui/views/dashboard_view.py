from cli.tui.base_element import BaseElement
from utils.state import AppState
from datetime import datetime
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Layout, Label, Divider, ListBox, Button, VerticalDivider
from asciimatics.exceptions import NextScene, StopApplication
from cli.tui.scene_type import SceneType

class DashboardView(BaseElement):
    def __init__(self, screen: Screen, state: AppState) -> None:
        super().__init__(screen, state, title="📊 Personal Assistant")

        # --- Верхня секція: Статистика ---
        stats_layout = Layout([1, 1, 1])
        self.add_layout(stats_layout)
        stats = self._state.get_stats()
        stats_layout.add_widget(Label(f"👥 Контактів: {stats['contacts']}"), 0)
        stats_layout.add_widget(Label(f"📝 Нотаток: {stats['notes']}"), 1)
        stats_layout.add_widget(Label(f"📅 Сьогодні: {datetime.now().strftime('%d.%m.%Y')}"), 2)
        
        self.add_layout(Layout([1])) # Проміжний шар

        divider_layout = Layout([1])
        self.add_layout(divider_layout)
        divider_layout.add_widget(Divider())

        # --- Середня секція: Нагадування та Меню ---
        main_layout = Layout([1, 1], fill_frame=True)
        self.add_layout(main_layout)
        
        # Ліва колонка: Дні народження
        main_layout.add_widget(Label("🎂 НАЙБЛИЖЧІ ДНІ НАРОДЖЕННЯ:"), 0)
        main_layout.add_widget(Divider(draw_line=False), 0)
        bdays = self._state.address_book_manager.get_upcoming_birthdays()
        for b in bdays:
            main_layout.add_widget(Label(f"  • {b}"), 0)

        # Права колонка: Швидке меню
        main_layout.add_widget(Label("Оберіть дію (використовуйте стрілки та Enter):"), 1)
        main_layout.add_widget(Divider(draw_line=False), 1)

        options = [
            ("👥 Контакти", SceneType.CONTACTS_LIST),
            ("🎂 Дні народження", SceneType.BIRTHDAYS_LIST),
            ("📝 Нотатки", SceneType.NOTES_LIST),
            ("❌ Вихід (Q)", 0)
        ]
        
        self._list = ListBox(len(options), options,
                             name="menu", on_select=self._on_click)
        main_layout.add_widget(self._list, 1)

        # --- Нижня секція: Кнопка дії ---
        footer = Layout([1])
        self.add_layout(footer)
        footer.add_widget(Divider())
        footer.add_widget(Button("ПЕРЕЙТИ", self._on_click))
        
        self.fix()
    
    def process_event(self, event) -> None:
        if isinstance(event, KeyboardEvent):
            if event.key_code in self._exit_key_codes:
                raise StopApplication("User quit via key code")
        
        return super().process_event(event)

    def _on_click(self) -> None:
        sceneOrExit = self._list.value

        if sceneOrExit == 0:
            raise StopApplication("User quit via menu")
        
        raise NextScene(sceneOrExit)
