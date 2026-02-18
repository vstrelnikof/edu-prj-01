from utils.state import AppState
from asciimatics.widgets import Layout, Text, Button, TextBox, PopUpDialog
from asciimatics.exceptions import NextScene
from cli.tui.base_element import BaseElement
from cli.tui.scene_type import SceneType
from utils.validator import Validator

class BaseForm(BaseElement):
    required_fields: list[str] = []

    def __init__(self, screen, state: AppState, **kwargs):
        super().__init__(screen, state,
                         height=screen.height // 2,
                         width=screen.width // 2,
                        #  hover_focus=True,
                         has_shadow=True,
                         is_modal=True,
                         **kwargs)

    def complete(self):
        layout = Layout([1, 1])
        self.add_layout(layout)
        layout.add_widget(Button("Зберегти", self._ok), 0)
        layout.add_widget(Button("Скасувати", self._cancel), 1)
        self.fix()

    def validate_form(self) -> bool:
        for field_name in self.required_fields:
            widget = self.find_widget(field_name)
            if widget and hasattr(widget, "is_valid") and not widget.is_valid:
                self.add_effect(
                    PopUpDialog(self._screen, f"❌ Поле '{widget.label}' заповнено некоректно!", ["Виправити"])
                )
                return False
        return True

    def _ok(self):
        self.save()

    def _cancel(self):
        raise NextScene(SceneType.MAIN)
