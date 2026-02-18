from asciimatics.widgets import Frame, Layout, Text, Button, TextBox
from asciimatics.exceptions import NextScene

from cli.tui.scene_type import SceneType

class NoteForm(Frame):
    def __init__(self, screen, manager):
        super().__init__(screen, screen.height // 2, screen.width // 2,
                         hover_focus=True, title="📝 Нова нотатка")
        self._manager = manager
        self.set_theme("bright")

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        # TextBox для багаторядкового тексту
        layout.add_widget(TextBox(5, label="Текст:", name="text", as_string=True))
        layout.add_widget(Text("Теги (через кому):", name="tags"))

        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Зберегти", self._ok), 0)
        layout2.add_widget(Button("Скасувати", self._cancel), 1)
        self.fix()

    def _ok(self):
        if not self.data: return
        
        self.save()
        # Перетворюємо рядок тегів у список
        if isinstance(self.data["tags"], str):
            self.data["tags"] = [t.strip() for t in self.data["tags"].split(",") if t.strip()]
        
        self._manager.add_note_from_dict(self.data)
        raise NextScene(SceneType.MAIN)

    def _cancel(self):
        raise NextScene(SceneType.MAIN)
