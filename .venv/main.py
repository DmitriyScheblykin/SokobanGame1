import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QMessageBox
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt

EMPTY = 0
WALL = 1
BOX = 2
GOAL = 3
PLAYER = 4
BOX_ON_GOAL = 5
PLAYER_ON_GOAL = 6

tile_images = {
    EMPTY: "empty.png",
    WALL: "wall.png",
    BOX: "box.png",
    GOAL: "goal.png",
    PLAYER: "player.png",
    BOX_ON_GOAL: "box_on_goal.png",
    PLAYER_ON_GOAL: "player_on_goal.png",
}

levels = {
    "Level 1": [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 3, 2, 0, 0, 1],
        [1, 0, 0, 4, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ],
    "Level 2": [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 3, 0, 0, 1],
        [1, 0, 0, 2, 0, 2, 0, 1],
        [1, 0, 4, 0, 2, 0, 0, 1],
        [1, 0, 0, 0, 3, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "Level 3": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 3, 0, 2, 0, 0, 1],
        [1, 0, 0, 2, 0, 0, 0, 0, 1],
        [1, 0, 4, 0, 2, 0, 0, 0, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 3, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "Level 4": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 2, 0, 1],
        [1, 0, 1, 3, 3, 1, 1, 1, 0, 4, 2, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
}


class SokobanGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игра Сокобан")
        self.setGeometry(600, 200, 200, 200)

        self.current_level = "Level 1"
        self.player_position = (3, 3)
        self.box_positions = [(2, 2)]

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.game_board_layout = QHBoxLayout()
        self.main_layout.addLayout(self.game_board_layout)

        self.game_board = QLabel()
        self.game_board_layout.addWidget(self.game_board)

        self.control_layout = QHBoxLayout()
        self.main_layout.addLayout(self.control_layout)

        self.menu_button = QPushButton("Меню")
        self.control_layout.addWidget(self.menu_button)
        self.menu_button.clicked.connect(self.show_menu)

        self.prev_level_button = QPushButton("Предыдущий уровень")
        self.control_layout.addWidget(self.prev_level_button)
        self.prev_level_button.clicked.connect(self.load_previous_level)

        self.next_level_button = QPushButton("Следующий уровень")
        self.control_layout.addWidget(self.next_level_button)
        self.next_level_button.clicked.connect(self.load_next_level)

        self.load_level(self.current_level)
        self.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.move_player(-1, 0)
        elif event.key() == Qt.Key_Down:
            self.move_player(1, 0)
        elif event.key() == Qt.Key_Left:
            self.move_player(0, -1)
        elif event.key() == Qt.Key_Right:
            self.move_player(0, 1)

    def move_player(self, dx, dy):
        new_player_position = (self.player_position[0] + dx, self.player_position[1] + dy)
        level_data = levels[self.current_level]

        if self.is_valid_move(new_player_position, dx, dy):
            if level_data[new_player_position[0]][new_player_position[1]] in [BOX, BOX_ON_GOAL]:
                box_new_position = (new_player_position[0] + dx, new_player_position[1] + dy)
                if self.is_valid_move(box_new_position, dx, dy):
                    # движение ящиков
                    if level_data[box_new_position[0]][box_new_position[1]] == GOAL:
                        level_data[box_new_position[0]][box_new_position[1]] = BOX_ON_GOAL
                    else:
                        level_data[box_new_position[0]][box_new_position[1]] = BOX

                    if level_data[new_player_position[0]][new_player_position[1]] == BOX_ON_GOAL:
                        level_data[new_player_position[0]][new_player_position[1]] = PLAYER_ON_GOAL
                    else:
                        level_data[new_player_position[0]][new_player_position[1]] = PLAYER

            if level_data[self.player_position[0]][self.player_position[1]] == PLAYER_ON_GOAL:
                level_data[self.player_position[0]][self.player_position[1]] = GOAL
            else:
                level_data[self.player_position[0]][self.player_position[1]] = EMPTY

            if level_data[new_player_position[0]][new_player_position[1]] == GOAL:
                level_data[new_player_position[0]][new_player_position[1]] = PLAYER_ON_GOAL
            else:
                level_data[new_player_position[0]][new_player_position[1]] = PLAYER

            self.player_position = new_player_position
            self.update_game_state()

    def is_valid_move(self, position, dx, dy):
        row, col = position
        if row < 0 or row >= len(levels[self.current_level]) or col < 0 or col >= len(levels[self.current_level][0]):
            return False

        tile_type = levels[self.current_level][row][col]

        if tile_type == WALL:
            return False

        if tile_type in [BOX, BOX_ON_GOAL]:
            new_box_position = (row + dx, col + dy)
            if new_box_position[0] < 0 or new_box_position[0] >= len(levels[self.current_level]) or new_box_position[
                1] < 0 or new_box_position[1] >= len(levels[self.current_level][0]):
                return False
            new_box_tile = levels[self.current_level][new_box_position[0]][new_box_position[1]]
            if new_box_tile in [WALL, BOX, BOX_ON_GOAL]:
                return False
            if tile_type == BOX_ON_GOAL and new_box_tile != GOAL:
                return False
        return True

    def update_game_state(self):
        level_data = levels[self.current_level]
        self.game_board.setPixmap(self.create_game_board(level_data))
        self.check_victory()

    def check_victory(self):
        level_data = levels[self.current_level]
        if all(level_data[row][col] in [BOX_ON_GOAL, PLAYER_ON_GOAL, EMPTY, WALL, PLAYER] for row in
               range(len(level_data)) for col in range(len(level_data[row]))):
            if all((level_data[row][col] != GOAL and level_data[row][col] != BOX) for row in range(len(level_data)) for
                   col in range(len(level_data[row]))):
                self.victory_message()

    def create_game_board(self, level_data):
        board_size = (70, 70)
        board_width = len(level_data[0]) * board_size[0]
        board_height = len(level_data) * board_size[1]
        board_pixmap = QPixmap(board_width, board_height)
        board_pixmap.fill(Qt.transparent)

        painter = QPainter(board_pixmap)
        for row in range(len(level_data)):
            for col in range(len(level_data[row])):
                tile_type = level_data[row][col]
                tile_image = tile_images[tile_type]
                tile_x = col * board_size[0]
                tile_y = row * board_size[1]
                painter.drawPixmap(tile_x, tile_y, board_size[0], board_size[1], QPixmap(tile_image))

        painter.end()
        return board_pixmap

    def load_previous_level(self):
        level_names = list(levels.keys())
        current_index = level_names.index(self.current_level)
        if current_index > 0:
            self.load_level(level_names[current_index - 1])
            self.setFocus()

    def load_next_level(self):
        level_names = list(levels.keys())
        current_index = level_names.index(self.current_level)
        if current_index < len(level_names) - 1:
            self.load_level(level_names[current_index + 1])
            self.setFocus()

    def load_level(self, level_name):
        self.current_level = level_name
        self.player_position = None
        self.box_positions = []

        level_data = levels[level_name]
        self.game_board.setPixmap(self.create_game_board(level_data))

        for row in range(len(level_data)):
            for col in range(len(level_data[row])):
                if level_data[row][col] == PLAYER:
                    self.player_position = (row, col)
                elif level_data[row][col] == BOX:
                    self.box_positions.append((row, col))

        self.update_game_state()

    def show_menu(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Меню")
        msgBox.setText("Выберите уровень:")

        level_buttons = {}
        for level_name in levels:
            button = msgBox.addButton(level_name, QMessageBox.AcceptRole)
            level_buttons[button] = level_name

        msgBox.addButton("Отмена", QMessageBox.RejectRole)

        msgBox.exec_()

        for button, level_name in level_buttons.items():
            if msgBox.clickedButton() == button:
                self.load_level(level_name)
                break

        self.setFocus()

    def victory_message(self):
        level_data = levels[self.current_level]
        all(
            level_data[row][col] != GOAL for row in range(len(level_data)) for col in range(len(level_data[row])))
        if all(level_data[row][col] in [BOX_ON_GOAL, PLAYER_ON_GOAL, EMPTY, WALL, PLAYER] for row in
               range(len(level_data)) for col in range(len(level_data[row])) if level_data[row][col] == GOAL):
            QMessageBox.information(self, "Победа!!", "Уровень пройден!")
            self.show_menu()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SokobanGame()
    game.show()
    sys.exit(app.exec_())
