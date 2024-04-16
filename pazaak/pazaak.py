from random import choice, shuffle
from sys import exit

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from ui_game import Ui_main_win


MODS = ['+', '-', '-/+']


class Card:
    def __init__(
            self,
            num: int,
            mod: str = None,
            is_dual: bool = None
            ) -> None:
        self.num = num
        self.mod = mod
        self.is_dual = is_dual
        if mod == '-/+':
            self.current_mod = choice(MODS[:2])

    def __str__(self) -> str:
        s = 'Card: '
        if self.mod:
            s += self.mod
        s += str(self.num)
        if self.mod == '-/+':
            s += f' (Current Mod: {self.current_mod})'
        return s

    def flip_mod(self):
        """Flip the current modifier on dual cards."""
        if self.current_mod == '+':
            self.current_mod = '-'
        else:
            self.current_mod = '+'


class Competitor:
    def __init__(
            self,
            name: str,
            is_standing = False
            ) -> None:
        self.name = name
        self.is_standing = is_standing


class Game:
    side_deck = []

    @classmethod
    def add_to_side_deck(cls):
        button_name = ui.sender().objectName()
        print('[Debug LOG] Button pressed:', button_name)

    @classmethod
    def gen_random_side_deck(cls):
        ...

    @classmethod
    def get_main_deck(cls, repetitions: int = 8) -> None:
        """Generate a list of cards representing the house's deck.

        The optional parameter 'repetitions' shuffles it that many times.
        """

        cls.main_deck = []
        for n in range(10):
            for _ in range(4):
                cls.main_deck.append(Card(n + 1))
        for _ in range(repetitions):
            shuffle(cls.main_deck)


class Pazaak(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon('assets/app_icon.png'))
        self.ui = Ui_main_win()
        self.ui.setupUi(self)
        self.ui.btn_play.clicked.connect(self.play)
        self.ui.btn_help.clicked.connect(self.go_to_help)
        self.ui.btn_quit_game.clicked.connect(QtWidgets.QApplication.quit)
        self.ui.btn_help_to_main.clicked.connect(self.go_to_main)
        self.ui.btn_deck_to_main.clicked.connect(self.go_to_main)
        self.ui.btn_start_match.clicked.connect(self.start_match)
        self.ui.btn_quit_match.clicked.connect(self.go_to_main)

        card_buttons = [self.ui.btn_card_plus_1, self.ui.btn_card_plus_2,
                        self.ui.btn_card_plus_3, self.ui.btn_card_plus_4,
                        self.ui.btn_card_plus_5, self.ui.btn_card_plus_6,
                        self.ui.btn_card_minus_1, self.ui.btn_card_minus_2,
                        self.ui.btn_card_minus_3, self.ui.btn_card_minus_4,
                        self.ui.btn_card_minus_5, self.ui.btn_card_minus_6,
                        self.ui.btn_card_dual_1, self.ui.btn_card_dual_2,
                        self.ui.btn_card_dual_3, self.ui.btn_card_dual_4,
                        self.ui.btn_card_dual_5, self.ui.btn_card_dual_6]
        for button in card_buttons:
            button.clicked.connect(Game.add_to_side_deck)
    
    def go_to_help(self):
        self.ui.stacked_widget.setCurrentIndex(1)
    
    def go_to_main(self):
        self.ui.stacked_widget.setCurrentIndex(0)

    def play(self):
        # TODO: Logic for starting a new game from the main menu.
        self.ui.stacked_widget.setCurrentIndex(2)

    def start_match(self):
        # TODO: Logic for starting a new match from the deck selection screen.
        self.ui.stacked_widget.setCurrentIndex(3)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ui = Pazaak()
    ui.show()
    exit(app.exec_())
