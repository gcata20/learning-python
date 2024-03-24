import inspect
import random
import sys


NUM_OF_DIGITS = 3
MAX_GUESSES = 10


def main():
    intro_msg = inspect.cleandoc(f'''
        How to play:
        Guess a random {NUM_OF_DIGITS}-digit number with no repeating digits.
        You have a total of {MAX_GUESSES} guesses.
                                 
        The following clues will be provided after each attempt:
        - Pico: one digit is correct but in the wrong place
        - Fermi: one digit is correct and in the right place
        - Bagels: no digits are correct
        ''')
    print(intro_msg)

    # Main game loop.
    while True:
        secret_num = get_secret_num()
        print()
        print('I thought of a number. Can you guess it?')

        # Round loop.
        num_of_guesses = 1
        while num_of_guesses <= MAX_GUESSES:
            # Guess input loop.
            while True:
                guess = input(f'Guess #{num_of_guesses}: ').strip()
                if not guess.isdecimal() or len(guess) != NUM_OF_DIGITS:
                    print(f'Please input a {NUM_OF_DIGITS}-digit number.')
                    continue
                break
            # Win condition check.
            if guess == secret_num:
                print('You guessed it. Congratulations!')
                break
            # Guess processing.
            clues = get_clues(guess, secret_num)
            print(clues)
            num_of_guesses += 1
            # Loss condition check.
            if num_of_guesses > MAX_GUESSES:
                print(f'You lost. The correct answer was: {secret_num}.')
        
        # Replay input loop.
        print('Would you like to play again? (y/n):')
        while True:
            match input('-> ').strip().lower():
                case 'y':
                    break
                case 'n':
                    print('Thank you for playing.')
                    sys.exit(0)
                case _:
                    print('Please input y or n.')
                    continue


def get_clues(guess: str, secret_num: str) -> str:
    """Return a str of clues."""
    clues = []
    for i in range(NUM_OF_DIGITS):
        if guess[i] == secret_num[i]:
            clues.append('Fermi.')
        elif guess[i] in secret_num:
            clues.append('Pico.')
    if not clues:
        return 'Bagels.'
    clues.sort()
    return ' '.join(clues)


def get_secret_num() -> str:
    """Return a str with NUM_DIGITS length made from random, unique digits."""
    secret_num = ''
    while len(secret_num) < NUM_OF_DIGITS:
        n = str(random.randint(0, 9))
        if n not in secret_num:
            secret_num += n
    return secret_num


if __name__ == '__main__':
    main()
