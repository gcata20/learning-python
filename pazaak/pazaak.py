from random import choice, shuffle
from sys import exit

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap

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
        self.img_path = f'assets/card_{MOD_DICT[mod]}_{num}.png'
        if mod == '-/+':
            self.is_dual = True
            self.current_mod = choice(MODS[:2])
            self.set_img()
        else:
            self.current_mod = mod

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
        self.set_img()

    def set_img(self):
        if self.current_mod == '+':
            dual_mod_text = 'pm'
        else:
            dual_mod_text = 'mp'
        self.img_path = f'assets/card_{dual_mod_text}_{self.num}.png'


class Competitor:
    def __init__(self, name: str) -> None:
        self.name = name
        self.total = 0
        self.has_played_card = False
        self.is_standing = False
        self.hand_cards = [None] * 4
        self.sets_won = 0
        self.generate_hand()
    
    def generate_hand(self):
        for _ in range(8):
            shuffle(SideDeckManager.side_deck)
        for i in range(4):
            side_deck_card = SideDeckManager.side_deck.pop()
            mod = side_deck_card[:-1]
            num = side_deck_card[-1]
            new_card = Card(num, mod)
            self.hand_cards[i] = new_card


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
        main_win.ui.popup_match_status.hide()
        main_win.ui.stacked_widget.setCurrentIndex(0)

    @classmethod
    def play(cls):
        SideDeckManager.clear_deck()
        main_win.ui.stacked_widget.setCurrentIndex(2)
    
    @classmethod
    def start_match(cls):
        MatchManager.init_match()
        main_win.ui.stacked_widget.setCurrentIndex(3)


class MatchManager:
    main_deck = []
    player_hand = [Card] * 4
    set_is_over = False
    match_is_over = False

    @classmethod
    def check_end_conditions(cls):
        player_total = int(main_win.ui.player_total.text())
        computer_total = int(main_win.ui.computer_total.text())
        
        if player_total > 20:
            cls.set_is_over = True
            cls.computer.sets_won += 1
            main_win.ui.text_info_set.setText('You lost the set.')
        elif cls.computer.is_standing and computer_total > 20:
            cls.set_is_over = True
            cls.player.sets_won += 1
            main_win.ui.text_info_set.setText('You won the set.')
        elif cls.player.is_standing and cls.computer.is_standing:
            if player_total == computer_total:
                cls.set_is_over = True
                main_win.ui.text_info_set.setText('The set is a draw.')
            elif player_total > computer_total:
                cls.set_is_over = True
                cls.player.sets_won += 1
                main_win.ui.text_info_set.setText('You won the set.')
            elif player_total < computer_total:
                cls.set_is_over = True
                cls.computer.sets_won += 1
                main_win.ui.text_info_set.setText('You lost the set.')

        if cls.player.sets_won == 3:
            cls.match_is_over = True
            main_win.ui.text_info_match.setText('You won the match.')
        elif cls.computer.sets_won == 3:
            cls.match_is_over = True
            main_win.ui.text_info_match.setText('You lost the match.')
            
        if cls.match_is_over:
            QtCore.QTimer.singleShot(800, cls.show_match_status)
        elif cls.set_is_over:
            QtCore.QTimer.singleShot(800, cls.show_set_status)

    @classmethod
    def end_turn(cls):
        cls.toggle_buttons(False)
        cls.check_end_conditions()
        if cls.set_is_over or cls.match_is_over:
            return
        if not cls.computer.is_standing:
            QtCore.QTimer.singleShot(100, cls.run_computer_turn)
        else:
            cls.run_player_turn()

    @classmethod
    def flip_card(cls):
        button_index = int(main_win.sender().objectName()[-1]) - 1
        card_to_flip = cls.player.hand_cards[button_index]
        card_to_flip.flip_mod()
        img_path = card_to_flip.img_path
        main_win.player_hand_buttons[button_index].setIcon(QIcon(img_path))

    @classmethod
    def gen_main_deck(cls, repetitions: int = 8) -> None:
        """Generate a list of cards representing the house's deck.

        The optional parameter 'repetitions' shuffles it that many times.
        """

        cls.main_deck.clear()
        for n in range(10):
            for _ in range(4):
                cls.main_deck.append(n + 1)
        for _ in range(repetitions):
            shuffle(cls.main_deck)
    
    @classmethod
    def init_match(cls):
        main_win.ui.popup_set_status.hide()
        cls.match_is_over = False
        cls.player = Competitor('player')
        cls.computer = Competitor('computer')

        # Reset turn, set and total value indicators.
        indicators = [main_win.ui.player_turn, main_win.ui.computer_turn,
                      main_win.ui.player_set_1, main_win.ui.player_set_2,
                      main_win.ui.player_set_3, main_win.ui.computer_set_1,
                      main_win.ui.computer_set_2, main_win.ui.computer_set_3]
        for label in indicators:
            label_name = label.objectName()
            if 'turn' in label_name:
                label_type = 'turn'
            else:
                label_type = 'set'
            img_path = f'assets/{label_type}_inactive.png'
            label.setPixmap(QPixmap(img_path))
        for label in [main_win.ui.player_total, main_win.ui.computer_total]:
            label.setText('0')

        # Initialize player's hand card images.
        player_card_buttons = [main_win.ui.player_hand_1,
                               main_win.ui.player_hand_2,
                               main_win.ui.player_hand_3,
                               main_win.ui.player_hand_4]
        player_flip_buttons = [main_win.ui.player_hand_flip_1,
                               main_win.ui.player_hand_flip_2,
                               main_win.ui.player_hand_flip_3,
                               main_win.ui.player_hand_flip_4]
        for index, button in enumerate(player_card_buttons):
            button.setEnabled(True)
            button.setIcon(QIcon(cls.player.hand_cards[index].img_path))
            if cls.player.hand_cards[index].is_dual:
                player_flip_buttons[index].setEnabled(True)
                player_flip_buttons[index].setIcon(QIcon('assets/flip.png'))
            else:
                player_flip_buttons[index].setIcon(QIcon())
                player_flip_buttons[index].setEnabled(False)

        # Initialize computer's hand card images.
        computer_card_labels = [main_win.ui.computer_hand_1,
                                main_win.ui.computer_hand_2,
                                main_win.ui.computer_hand_3,
                                main_win.ui.computer_hand_4]
        for label in computer_card_labels:
            label.setPixmap(QPixmap('assets/card_back.png'))
        
        cls.gen_main_deck()
        cls.start_set()

    @classmethod
    def init_table(cls):
        table_slots = main_win.player_table_slots + main_win.comp_table_slots
        for label in table_slots:
            label.setPixmap(QPixmap())
            label.setEnabled(False)
        for label in [main_win.ui.player_total, main_win.ui.computer_total]:
            label.setText('0')

    @classmethod
    def play_card(cls):
        if cls.player.has_played_card:
            return
        button_index = int(main_win.sender().objectName()[-1]) - 1
        card_to_play = cls.player.hand_cards[button_index]
        main_win.player_hand_buttons[button_index].setIcon(QIcon())
        main_win.player_hand_buttons[button_index].setEnabled(False)
        if card_to_play.is_dual:
            main_win.player_card_flip_buttons[button_index].setIcon(QIcon())
            main_win.player_card_flip_buttons[button_index].setEnabled(False)
        for slot in main_win.player_table_slots:
            if not slot.isEnabled():
                slot.setEnabled(True)
                slot.setPixmap(QPixmap(card_to_play.img_path))
                break
        current_total = int(main_win.ui.player_total.text())
        card_num = int(card_to_play.num)
        if card_to_play.current_mod == '+':
            new_total = current_total + card_num
        else:
            new_total = current_total - card_num
        main_win.ui.player_total.setText(str(new_total))
        cls.player.hand_cards[button_index] = None
        cls.player.has_played_card = True
        if new_total == 20:
            cls.stand()
        elif main_win.player_table_slots[8].isEnabled():
            cls.stand()

    @classmethod
    def run_computer_turn(cls):
        if not cls.computer.is_standing:
            cls.update_turn_ui(False)
            drawn_card_value = cls.main_deck.pop()
            img_path = f'assets/card_base_{drawn_card_value}.png'
            for slot in main_win.comp_table_slots:
                if not slot.isEnabled():
                    slot.setEnabled(True)
                    slot.setPixmap(QPixmap(img_path))
                    break
            current_total = int(main_win.ui.computer_total.text())
            new_total = current_total + drawn_card_value
            main_win.ui.computer_total.setText(str(new_total))

            # TODO: ADD MORE LOGIC TO PLAY CARDS HERE DEPENDING ON TOTAL VALUE AND HAND CARDS (FOR COMPUTER).
            player_total = int(main_win.ui.player_total.text())
            if main_win.comp_table_slots[8].isEnabled():
                cls.computer.is_standing = True
            elif cls.player.is_standing:
                if player_total < new_total < 21:
                    cls.computer.is_standing = True
                elif player_total >= 17 and player_total == new_total:
                    cls.computer.is_standing = True
                elif player_total == 20:
                    pass
            elif 17 <= new_total < 21:
                cls.computer.is_standing = True

            # Temporary line to stop computer from drawing cards forever. :D
            # TODO: Replace with hand_card logic that tries to subtract from totals over 20.
            if new_total > 20:
                cls.computer.is_standing = True
        print('[DEBUG LOG] computer standing status:', cls.computer.is_standing)
        cls.check_end_conditions()
        if cls.set_is_over or cls.match_is_over:
            return
        QtCore.QTimer.singleShot(1000, cls.run_player_turn)

    @classmethod
    def run_player_turn(cls):
        cls.player.has_played_card = False
        if not cls.player.is_standing:
            cls.update_turn_ui(True)
            cls.toggle_buttons(True)
            drawn_card_value = cls.main_deck.pop()
            img_path = f'assets/card_base_{drawn_card_value}.png'
            for slot in main_win.player_table_slots:
                if not slot.isEnabled():
                    slot.setEnabled(True)
                    slot.setPixmap(QPixmap(img_path))
                    break
            current_total = int(main_win.ui.player_total.text())
            new_total = current_total + drawn_card_value
            main_win.ui.player_total.setText(str(new_total))
            if new_total == 20:
                cls.stand()
            elif main_win.player_table_slots[8].isEnabled():
                cls.stand()
        else:
            QtCore.QTimer.singleShot(100, cls.run_computer_turn)
    
    @classmethod
    def show_match_status(cls):
        cls.update_set_ui()
        main_win.ui.popup_match_status.show()
    
    @classmethod
    def show_set_status(cls):
        cls.update_set_ui()
        main_win.ui.popup_set_status.show()

    @classmethod
    def stand(cls):
        cls.player.is_standing = True
        cls.end_turn()
    
    @classmethod
    def start_set(cls):
        main_win.ui.popup_set_status.hide()
        cls.init_table()
        cls.set_is_over = False
        cls.player.is_standing = False
        cls.computer.is_standing = False
        QtCore.QTimer.singleShot(500, cls.run_player_turn)

    @classmethod
    def toggle_buttons(cls, new_state: bool):
        for button in main_win.game_buttons:
            button.setEnabled(new_state)
        for i, button in enumerate(main_win.player_hand_buttons):
            if cls.player.hand_cards[i]:
                button.setEnabled(new_state)
        for i, button in enumerate(main_win.player_card_flip_buttons):
            if cls.player.hand_cards[i] and cls.player.hand_cards[i].is_dual:
                button.setEnabled(new_state)

    @classmethod
    def update_set_ui(cls):
        img_path = 'assets/set_active.png'
        if cls.player.sets_won > 0:
            index = cls.player.sets_won - 1
            main_win.player_set_indicators[index].setPixmap(QPixmap(img_path))
        if cls.computer.sets_won > 0:
            index = cls.computer.sets_won - 1
            main_win.comp_set_indicators[index].setPixmap(QPixmap(img_path))

    @classmethod
    def update_turn_ui(cls, is_players_turn: bool):
        active_img_path = 'assets/turn_active.png'
        inactive_img_path = 'assets/turn_inactive.png'
        if is_players_turn:
            main_win.ui.computer_turn.setPixmap(QPixmap(inactive_img_path))
            main_win.ui.player_turn.setPixmap(QPixmap(active_img_path))
        else:
            main_win.ui.player_turn.setPixmap(QPixmap(inactive_img_path))
            main_win.ui.computer_turn.setPixmap(QPixmap(active_img_path))


class Pazaak(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon('assets/app_icon.png'))
        self.ui = Ui_main_win()
        self.ui.setupUi(self)

        self.ui.popup_match_status.hide()
        self.ui.popup_set_status.hide()

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
        self.ui.btn_end_turn.clicked.connect(MatchManager.end_turn)
        self.ui.btn_stand.clicked.connect(MatchManager.stand)
        self.ui.btn_quit_match.clicked.connect(GameManager.go_to_main)

        self.game_buttons = [self.ui.btn_end_turn,
                             self.ui.btn_stand,
                             self.ui.btn_quit_match]

        self.player_hand_buttons = [self.ui.player_hand_1,
                                    self.ui.player_hand_2,
                                    self.ui.player_hand_3,
                                    self.ui.player_hand_4]
        for btn in self.player_hand_buttons:
            btn.clicked.connect(MatchManager.play_card)
        self.player_card_flip_buttons = [self.ui.player_hand_flip_1,
                                         self.ui.player_hand_flip_2,
                                         self.ui.player_hand_flip_3,
                                         self.ui.player_hand_flip_4]
        for btn in self.player_card_flip_buttons:
            btn.clicked.connect(MatchManager.flip_card)

        # Game screen card slots.
        self.player_table_slots = [self.ui.player_slot_1,
                                   self.ui.player_slot_2,
                                   self.ui.player_slot_3,
                                   self.ui.player_slot_4,
                                   self.ui.player_slot_5,
                                   self.ui.player_slot_6,
                                   self.ui.player_slot_7,
                                   self.ui.player_slot_8,
                                   self.ui.player_slot_9]
        self.comp_table_slots = [self.ui.computer_slot_1,
                                 self.ui.computer_slot_2,
                                 self.ui.computer_slot_3,
                                 self.ui.computer_slot_4,
                                 self.ui.computer_slot_5,
                                 self.ui.computer_slot_6,
                                 self.ui.computer_slot_7,
                                 self.ui.computer_slot_8,
                                 self.ui.computer_slot_9]

        # Game screen set indicators.
        self.player_set_indicators = [self.ui.player_set_1,
                                      self.ui.player_set_2,
                                      self.ui.player_set_3]
        self.comp_set_indicators = [self.ui.computer_set_1,
                                    self.ui.computer_set_2,
                                    self.ui.computer_set_3]

        # Set and match popups.
        self.ui.btn_ok_set.clicked.connect(MatchManager.start_set)
        self.ui.btn_ok_match.clicked.connect(GameManager.go_to_main)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main_win = Pazaak()
    main_win.show()
    exit(app.exec_())
