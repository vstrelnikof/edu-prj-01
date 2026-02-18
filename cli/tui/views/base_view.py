from utils.state import AppState
from abc import abstractmethod
from cli.tui.base_element import BaseElement
from asciimatics.screen import Screen
from asciimatics.widgets import Layout, MultiColumnListBox, Button, Divider, Text, PopUpDialog
from asciimatics.exceptions import NextScene
from cli.tui.scene_type import SceneType

class BaseView(BaseElement):
    _list_box: MultiColumnListBox
    
    def __init__(self, screen: Screen, state: AppState, **kwargs) -> None:
        super().__init__(screen, state, has_border=True, **kwargs)
        search_layout = Layout([1, 10, 1])
        self.add_layout(search_layout)
        # on_change викликає метод filter_list при кожному символі
        self._search_box = Text("🔎 Пошук: ", name="search", on_change=self._filter_list)
        search_layout.add_widget(self._search_box, 1)
        self._render_content()
        layout = Layout([1])
        self.add_layout(layout)
        layout.add_widget(Divider())
        button_layout = Layout([1, 1, 1, 1])
        self.add_layout(button_layout)
        button_layout.add_widget(Button("Створити", self._on_create), 0)
        button_layout.add_widget(Button("Редагувати", self._on_edit), 1)
        button_layout.add_widget(Button("Видалити", self._on_delete), 2)
        button_layout.add_widget(Button("Назад (ESC)", self._on_back), 3)
        self.fix()
    
    @abstractmethod
    def _render_content(self) -> None:
        pass

    @abstractmethod
    def _filter_list(self) -> None:
        """Фільтрація на основі тексту в пошуку."""
        pass
    
    def _on_create(self) -> None:
        pass
    
    def _on_edit(self) -> None:
        if self._list_box.value is None:
            return

        self._state.edit_index = self._list_box.value

    def _on_delete(self) -> None:
        assert self.scene is not None
        if self._list_box.value is None:
            return
        # Створюємо діалог підтвердження
        self.scene.add_effect(
            PopUpDialog(
                self._screen, 
                "❓Ви впевнені, що хочете видалити запис?", 
                ["Так", "Ні"],
                on_close=self._confirm_delete
            )
        )
    
    @abstractmethod
    def _confirm_delete(self, selected_button_idx) -> None:
        pass

    def _on_back(self) -> None:
        raise NextScene(SceneType.MAIN)
    
    def reset(self):
        # Цей метод викликається автоматично щоразу при переході на цю сцену!
        super().reset()
        self._filter_list()