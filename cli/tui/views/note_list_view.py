from utils.state import AppState
from datetime import datetime
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Label, Divider, ListBox, Button, VerticalDivider, Text, MultiColumnListBox
from asciimatics.exceptions import NextScene, StopApplication
from cli.tui.scene_type import SceneType
from managers.scene_manager import SceneManager

class NoteListView(Frame):
    def __init__(self, screen: Screen, state: AppState):
        super().__init__(screen, screen.height, screen.width, has_border=True, title="📓 Ваші нотатки")
        self._state = state
        
        layout_search = Layout([100])
        self.add_layout(layout_search)
        self._search = Text("🔍 Пошук (текст або #тег):", name="search", on_change=self._filter_notes)
        layout_search.add_widget(self._search)

        layout_list = Layout([100], fill_frame=True)
        self.add_layout(layout_list)
        self._list_box = MultiColumnListBox(
            screen.height - 8,
            [">70%", "<30%"],
            [],
            # header=["Зміст нотатки", "🏷 Теги"],
            name="note_list"
        )
        layout_list.add_widget(self._list_box)

        layout_btns = Layout([1, 1, 1])
        self.add_layout(layout_btns)
        layout_btns.add_widget(Button("Назад", self._on_back), 0)
        layout_btns.add_widget(Button("Видалити", self._on_delete), 2)
        
        self.fix()
        self._filter_notes()

    def _filter_notes(self):
        query = self._search.value.lower() if self._search.value else ""
        filtered = []
        for i, n in enumerate(self._state.notes_manager.notes):
            tags_str = ", ".join(n.tags)
            if query in n.text.lower() or any(query in t.lower() for t in n.tags):
                # Обрізаємо довгий текст для таблиці
                display_text = (n.text[:60] + '...') if len(n.text) > 60 else n.text
                filtered.append(([display_text, tags_str], i))
        self._list_box.options = filtered
    
    def _on_back(self):
       SceneManager.next(SceneType.MAIN)

    def _on_delete(self):
        if self._list_box.value is not None:
            self._state.notes_manager.notes.pop(self._list_box.value)
            self._state.notes_manager.save()
            self._filter_notes()
