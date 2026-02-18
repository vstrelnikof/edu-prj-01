import logging
from managers.scene_manager import SceneManager
from utils.state import AppState
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from cli.tui.scene_type import SceneType
from cli.tui.forms.contact_form import ContactForm
from cli.tui.forms.note_form import NoteForm
from cli.tui.views.dashboard_view import DashboardView
from cli.tui.views.contact_list_view import ContactListView
from cli.tui.views.note_list_view import NoteListView

logging.basicConfig(filename="assistant.log",
                    level=logging.DEBUG,
                    filemode="w",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")

app_state = AppState()

def demo(screen: Screen, state: AppState):
    # Створюємо екземпляри вікон
    scenes: list[Scene] = SceneManager.createScenes({
        SceneType.MAIN: DashboardView(screen, state),
        SceneType.ADD_CONTACT: ContactForm(screen, state),
        SceneType.LIST_CONTACTS: ContactListView(screen, state),
        SceneType.ADD_NOTE: NoteForm(screen, state),
        SceneType.LIST_NOTES: NoteListView(screen, state),
    })
    # Використовуємо палітру кольорів
    screen.play(scenes, stop_on_resize=True, repeat=True)

if __name__ == "__main__":
    logging.info("Starting personal assistant...")
    Screen.wrapper(demo, arguments=[app_state])