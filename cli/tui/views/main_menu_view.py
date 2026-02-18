from cli.tui.base_element import BaseElement
from cli.tui.scene_type import SceneType
from managers.scene_manager import SceneManager
from utils.state import AppState
from asciimatics.widgets import ListBox, Layout, Divider, Button, Label
from asciimatics.exceptions import StopApplication

class MainMenuView(BaseElement):
    def __init__(self, screen, state: AppState):
        super().__init__(screen, state, title="🚀 Personal Assistant v2.0")

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("Оберіть дію (використовуйте стрілки та Enter):"))
        layout.add_widget(Divider())
        
        options = [
            ("➕ Додати новий контакт", SceneType.ADD_CONTACT),
            ("📋 Показати всі контакти", SceneType.LIST_CONTACTS),
            ("🎂 Дні народження", SceneType.LIST_BIRTHDAYS),
            ("📔 Нотатки (в розробці)", SceneType.LIST_NOTES),
            ("❌ Вихід", 0)
        ]
        
        self._list = ListBox(screen.height - 8, options,
                             name="menu", on_select=self._on_click)
        layout.add_widget(self._list)
        layout.add_widget(Divider())
        layout.add_widget(Button("Виконати", self._on_click))
        
        self.fix()

    def _on_click(self):
        sceneOrExit = self._list.value

        if sceneOrExit == 0:
            raise StopApplication("User quit")
        
        raise SceneManager.next(str(sceneOrExit))

