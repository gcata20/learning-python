from dataclasses import dataclass
from os import system
from secrets import choice
from sys import exit


MAX_HEALTH = 7 


@dataclass
class Game:
    current_health: int
    game_over: dict
    known_invalid_letters: list
    known_valid_letters: list
    remaining_letters_count: int
    round_count: int
    word: str


def main():
    words = get_words()

    # Game loop.
    while True:
        g = init_game(words)

        # Round loop.
        while True:
            g.round_count += 1
            print(f'~ Round {g.round_count} ~ ')
            print(show_health(g.current_health))
            print('Word:', show_word(g.word, g.known_valid_letters))
            print(f'({len(g.word)}-letter word)')
            guess = get_guess(g.known_invalid_letters, g.known_valid_letters)
            print()
            process_guess(guess, g)
            if g.game_over['state']:
                print(g.game_over['msg'])
                break
        
        if not play_again():
            exit(0)


def get_guess(invalid_letters: list, valid_letters: list) -> str:
    """Prompts user for valid input and returns it."""

    previous_guesses = valid_letters + invalid_letters
    while True:
        user_input = input('Guess: ').strip().lower()
        if user_input and user_input not in previous_guesses:
            return user_input


def get_words() -> list[str]:
    """Reads lines from file into list and returns it."""

    try:
        with open('words.txt', 'r') as f:
            words = f.readlines()
    except FileNotFoundError:
        exit('File "words.txt" was not found.')
    if not words:
        exit('File "words.txt" must not be empty.')
    return words


def init_game(words: list[str]) -> Game:
    """
    Initializes the necessary variables for the start of a new game.
    Returns a new Game object containing them.
    """

    word = choice(words).strip().lower()
    return Game(
        MAX_HEALTH,
        {'state': False, 'msg': ''},
        [],
        [],
        len(set(word)),
        0,
        word
    )


def play_again() -> bool:
    """Prompts user for another game, returns decision as bool."""

    while True:
        user_input = input('Play again? (y/n): ').strip().lower()
        if user_input == 'y':
            system('cls')
            return True
        elif user_input == 'n':
            return False


def process_guess(guess: str, g: Game):
    """
    Processes the user's input by doing multiple things.
    - if user tried to guess a single letter:
        - if correct:
            - adds it to the known valid letters
            - subtracts from total letters remaining
            - sets game over if no letters remain
        - else:
            - adds it to the known invalid letters
            - reduces health by one
    - if user tried to guess the entire word:
        - if correct, sets game over
        - else, reduces health by one
    - sets game over if no health remains
    """

    length = len(guess)
    match length:
        case 1:
            if guess in g.word:
                g.known_valid_letters.append(guess)
                g.remaining_letters_count -= 1
                if g.remaining_letters_count == 0:
                    g.game_over['state'] = True
                    g.game_over['msg'] = 'You won by guessing all letters!'
            else:
                g.known_invalid_letters.append(guess)
                g.current_health -= 1
        case _ if length > 1:
            if guess == g.word:
                g.game_over['state'] = True
                g.game_over['msg'] = 'You won by guessing the word!'
            else:
                g.current_health -= 1
    if g.current_health == 0:
        g.game_over['state'] = True
        g.game_over['msg'] = 'You lost.'


def show_health(current_health: int) -> str:
    """Returns a str of full and empty heart emojis indicating health."""

    full_hearts = '❤️ ' * current_health
    empty_hearts = '🖤' * (MAX_HEALTH - current_health)
    return f'{full_hearts}{empty_hearts}'


def show_word(word: str, known_letters: list) -> str:
    """
    Returns a str made up of:
    - letters, if they've been previously guessed correctly
    - underscores, in place of letters not yet revealed
    """

    s = ''
    for letter in word:
        if letter in known_letters:
            s += letter.upper()
        else:
            s += '_'
    return s


if __name__ == '__main__':
    main()
