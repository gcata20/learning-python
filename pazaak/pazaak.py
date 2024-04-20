from random import choice, shuffle
from sys import exit

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from ui_game import Ui_main_win

MODS = ['+', '-', '-/+']
VALUES = ['1', '2', '3', '4', '5', '6']
MOD_DICT = {'plus': '+', 'minus': '-', 'dual': '-/+',
            '+': 'plus', '-': 'minus', '-/+': 'dual'}


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
        self.icon_path = f'assets/card_{MOD_DICT[mod]}_{num}.png'
        if mod == '-/+':
            self.is_dual = True
            self.current_mod = choice(MODS[:2])
            self.set_icon()

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
        self.set_icon()

    def set_icon(self):
        if self.current_mod == '+':
            temp = 'pm'
        else:
            temp = 'mp'
        self.icon_path = f'assets/card_{temp}_{self.num}.png'


class Competitor:
    def __init__(
            self,
            name: str,
            is_standing = False
            ) -> None:
        self.name = name
        self.is_standing = is_standing


class SideDeckManager:
    side_deck = [None] * 10
    deck_is_full = False

    @classmethod
    def clear_deck(cls):
        cls.set_ready_status(False)
        cls.side_deck = [None] * 10
        for button in main_win.chosen_card_buttons:
            button.setIcon(QIcon())
            button.setEnabled(False)

    @classmethod
    def gen_random_deck(cls):
        cls.clear_deck()
        for button in main_win.chosen_card_buttons:
            while True:
                mod = choice(MODS)
                num = choice(VALUES)
                new_card = mod + num
                if cls.side_deck.count(new_card) == 2:
                    continue
                break
            index_to_add = int(button.objectName()[-1]) - 1
            cls.side_deck[index_to_add] = new_card
            icon_path = f'assets/card_{MOD_DICT[mod]}_{num}.png'
            button.setEnabled(True)
            button.setIcon(QIcon(icon_path))
        cls.set_ready_status(True)
    
    @classmethod
    def modify_deck(cls):
        sender: QtWidgets.QPushButton = main_win.sender()
        sender_name = sender.objectName()
        if 'card' in sender_name:
            for button in main_win.chosen_card_buttons:
                if not button.isEnabled():
                    mod, num = sender_name.split('_')[-2:]
                    mod = MOD_DICT[mod]
                    card_value = mod + num
                    index_to_modify = int(button.objectName()[-1]) - 1
                    cls.side_deck[index_to_modify] = card_value
                    card_name = sender_name.lstrip('btn_')
                    icon_path = f'assets/{card_name}.png'
                    button.setEnabled(True)
                    button.setIcon(QIcon(icon_path))
                    if not any(item is None for item in cls.side_deck):
                        cls.set_ready_status(True)
                    break
        elif 'chosen' in sender_name:
            if cls.deck_is_full:
                cls.set_ready_status(False)
            index_to_modify = int(sender_name[-1]) - 1
            cls.side_deck[index_to_modify] = None
            sender.setIcon(QIcon())
            sender.setEnabled(False)
    
    @classmethod
    def set_ready_status(cls, is_ready: bool):
        cls.deck_is_full = is_ready
        main_win.ui.btn_start_match.setEnabled(is_ready)


class GameManager:
    @classmethod
    def go_to_help(cls):
        main_win.ui.stacked_widget.setCurrentIndex(1)
    
    @classmethod
    def go_to_main(cls):
        main_win.ui.stacked_widget.setCurrentIndex(0)

    @classmethod
    def play(cls):
        SideDeckManager.clear_deck()
        main_win.ui.stacked_widget.setCurrentIndex(2)
    
    @classmethod
    def start_match(cls):
        # TODO: Logic for starting a new match from the deck selection screen.
        main_win.ui.stacked_widget.setCurrentIndex(3)


class Match:
    main_deck = []

    @classmethod
    def gen_main_deck(cls, repetitions: int = 8) -> None:
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

        # Main menu screen buttons.
        self.ui.btn_play.clicked.connect(GameManager.play)
        self.ui.btn_help.clicked.connect(GameManager.go_to_help)
        self.ui.btn_quit_game.clicked.connect(QtWidgets.QApplication.quit)
        self.ui.btn_help_to_main.clicked.connect(GameManager.go_to_main)

        # Side deck builder screen buttons.
        self.ui.btn_start_match.clicked.connect(GameManager.start_match)
        self.ui.btn_clear.clicked.connect(SideDeckManager.clear_deck)
        self.ui.btn_randomize.clicked.connect(SideDeckManager.gen_random_deck)
        self.ui.btn_deck_to_main.clicked.connect(GameManager.go_to_main)
        available_card_buttons = [
            self.ui.btn_card_plus_1, self.ui.btn_card_plus_2,
            self.ui.btn_card_plus_3, self.ui.btn_card_plus_4,
            self.ui.btn_card_plus_5, self.ui.btn_card_plus_6,
            self.ui.btn_card_minus_1, self.ui.btn_card_minus_2,
            self.ui.btn_card_minus_3, self.ui.btn_card_minus_4,
            self.ui.btn_card_minus_5, self.ui.btn_card_minus_6,
            self.ui.btn_card_dual_1, self.ui.btn_card_dual_2,
            self.ui.btn_card_dual_3, self.ui.btn_card_dual_4,
            self.ui.btn_card_dual_5, self.ui.btn_card_dual_6]
        self.chosen_card_buttons = [
            self.ui.btn_chosen_1, self.ui.btn_chosen_2,
            self.ui.btn_chosen_3, self.ui.btn_chosen_4,
            self.ui.btn_chosen_5, self.ui.btn_chosen_6,
            self.ui.btn_chosen_7, self.ui.btn_chosen_8,
            self.ui.btn_chosen_9, self.ui.btn_chosen_10]
        side_deck_buttons = available_card_buttons + self.chosen_card_buttons
        for btn in side_deck_buttons:
            btn.clicked.connect(SideDeckManager.modify_deck)
        
        # Game screen buttons.
        self.ui.btn_quit_match.clicked.connect(GameManager.go_to_main)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main_win = Pazaak()
    main_win.show()
    exit(app.exec_())
