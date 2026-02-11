import sys
from PySide6.QtCore import Slot, QTimer
from PySide6.QtWidgets import QApplication

from game import Game
from view import MyGameView

# ==============================================================================
# CONTROLLER
# ==============================================================================

class MyGameController: # TODO: change name
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._connect_signals()

        # אם המשחק שלכם דורש שני קליקים (למשל דמקה: קליק לבחירה וקליק ליעד)
        # ייתכן שתצטרכו משתנה עזר כאן, למשל: self.selected_origin = None
        self.start_new_game()

    def _connect_signals(self):
        """
        Connects board buttons to the function handling their being clicked
        """
        # ודאו שהחיבור מתאים למבנה הגרפי שבחרתם ב-View
        pass

    def start_new_game(self):
        """ Starts a new game """
        self._model.reset_game()
        self._view.reset_view()

        # אם המחשב הוא השחקן הראשון, צריך לזמן אותו כאן
        pass

    @Slot()
    def _handle_human_move(self, row, col):
        """
        Handles the human's move. This function changes the most from game to game
        """
        # תארו את הלוגיקה של קלט המשתמש:
        # שימו לב שיש הבדל בין משחקים בהם מניחים כלי חדש, למשחקים בהם מזיזים כלי קיים

        # בסוף המהלך: נעלו את הלוח והפעילו טיימר לתור של המחשב
        pass

    def _handle_ai_move(self):
        """ Operates the computer agent's move """
        # תארו את התהליך:
        pass

    def _sync_board_view(self):
        """
        Updates the entire View to match the Model's board state.
        Critical for games where pieces move or change color.
        """
        # יש לעבור על כל התאים בלוח ולעדכן את התצוגה בהתאם למצבם במודל
        pass

    def _check_game_over(self):
        """ Checks whether the game is over and updates the view if needed """
        # קבלו את התוצאה מהמודל והציגו הודעה מתאימה ב-View
        pass

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    game_model = Game(play_mode='GREEDY', output_mode='SILENT')

    game_view = MyGameView()
    game_view.show()

    controller = MyGameController(model=game_model, view=game_view)

    sys.exit(app.exec())