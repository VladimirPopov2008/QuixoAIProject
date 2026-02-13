# ==============================================================================
# GRAPHIC VIEW
# ==============================================================================


import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,
                               QPushButton, QVBoxLayout, QLabel, QMessageBox)
from PySide6.QtCore import Slot, QTimer

import json
from game import Game


class MyGameView(QMainWindow):  # TODO: change name
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VLadimir's Quixo - Agent (X) vs Manual (O)")
        self.setFixedSize(400, 480)
        
        self.general_layout = QVBoxLayout()
        self._central_widget = QWidget(self)

    def _create_board_grid(self):
        """ Creates the grid for the game board """
        # כמה כפתורים צריך? איך הם מסודרים?
        pass

    def update_button(self, row, col, player_mark):
        """ Updates a specific button's appearance after a piece has been placed on it """
        #  מה קורה למשבצת כששמים בה כלי?
        # שינוי טקסט (X/O)? שינוי צבע? שינוי אייקון/תמונה?
        # האם המשחק מאפשר פינוי של משבצת, או רק מילוי?
        pass

    def reset_view(self):
        """ Clears the grid and prepares the system for a new game """
        # איך מנקים את הלוח הגרפי לקראת התצוגה התחלתית?
        pass