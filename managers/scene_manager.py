from asciimatics.exceptions import NextScene
from asciimatics.scene import Scene

class SceneManager:
    @staticmethod
    def next(name: str):
        raise NextScene(name)

    @staticmethod
    def createScenes(tui_elements: dict) -> list[Scene]:
        return [
            Scene([tui_element], -1, name=scene_id)
            for scene_id, tui_element in tui_elements.items()
        ]