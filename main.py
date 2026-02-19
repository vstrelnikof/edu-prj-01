import logging
from factories.scene_factory import SceneFactory
from utils.state import AppState
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from cli.tui.scene_type import SceneType
from cli.tui.forms.contact_form import ContactForm
from cli.tui.forms.note_form import NoteForm
from cli.tui.views.dashboard_view import DashboardView
from cli.tui.views.contact_list_view import ContactListView
from cli.tui.views.note_list_view import NoteListView
from cli.tui.views.birthday_list_view import BirthdayListView

logging.basicConfig(filename="assistant.log",
                    level=logging.DEBUG,
                    filemode="w",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")

app_state = AppState()

def demo(screen: Screen, state: AppState):
    # Створюємо екземпляри вікон
    scenes: list[Scene] = SceneFactory.createScenes({
        SceneType.MAIN: DashboardView(screen, state),
        SceneType.CONTACT_FORM: ContactForm(screen, state),
        SceneType.CONTACTS_LIST: ContactListView(screen, state),
        SceneType.BIRTHDAYS_LIST: BirthdayListView(screen, state),
        SceneType.NOTE_FORM: NoteForm(screen, state),
        SceneType.NOTES_LIST: NoteListView(screen, state),
    })
    # Використовуємо палітру кольорів
    screen.play(scenes, 
                stop_on_resize=True,
                repeat=True)

if __name__ == "__main__":
    logging.info("Starting personal assistant...")
    Screen.wrapper(demo, arguments=[app_state])