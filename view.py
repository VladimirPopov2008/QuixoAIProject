# ==============================================================================
# GRAPHIC VIEW
# ==============================================================================


import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,
                               QPushButton, QVBoxLayout, QLabel, QMessageBox)
from PySide6.QtCore import Slot, QTimer

import json
from game import Game


class QuixoGameView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VLadimir's Quixo - Agent (X) vs Manual (O)")
        self.setFixedSize(400, 480)

        self.general_layout = QVBoxLayout()
        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.general_layout)

        self.board_grid = QGridLayout()
        self.general_layout.addLayout(self.board_grid)

        self.buttons = []
        self._create_board_grid()

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_view)
        self.general_layout.addWidget(self.reset_button)

    def _create_board_grid(self):
        """ Creates the grid for the game board """
        for row in range(5):
            row_buttons = []
            for col in range(5):
                button = QPushButton()
                button.setFixedSize(60, 60)
                button.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center; vertical-align: middle;")

                # Add a dot to perimeter buttons
                if row == 0 or row == 4 or col == 0 or col == 4:
                    button.setText("•")  # Use a centered dot character

                button.clicked.connect(lambda checked, r=row, c=col: self.handle_button_click(r, c))
                self.board_grid.addWidget(button, row, col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def update_button(self, row, col, player_mark):
        """ Updates a specific button's appearance after a piece has been placed on it """
        button = self.buttons[row][col]
        button.setText(player_mark)
        if player_mark == "X":
            button.setStyleSheet("background-color: lightblue; font-size: 20px; font-weight: bold;")
        elif player_mark == "O":
            button.setStyleSheet("background-color: lightgreen; font-size: 20px; font-weight: bold;")
        else:
            button.setStyleSheet("font-size: 20px; font-weight: bold;")

    def reset_view(self):
        """ Clears the grid and prepares the system for a new game """
        for row in range(5):
            row_buttons = []
            for col in range(5):
                button = QPushButton()
                button.setFixedSize(60, 60)
                button.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center; vertical-align: middle;")

                # Add a dot to perimeter buttons
                if row == 0 or row == 4 or col == 0 or col == 4:
                    button.setText("•")  # Use a centered dot character

    @Slot()
    def handle_button_click(self, row, col):
        """ Handles the button click event """
        # Check if the button is on the perimeter
        if row == 0 or row == 4 or col == 0 or col == 4:
            QMessageBox.information(self, "Button Clicked", f"Button at ({row}, {col}) clicked!")
        else:
            QMessageBox.warning(self, "Invalid Move", "Only the edge buttons are allowed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = QuixoGameView()
    view.show()
    sys.exit(app.exec())