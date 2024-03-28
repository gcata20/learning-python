from random import choice, randint, shuffle


def main():
    house_deck = get_house_deck()
    player_hand = get_hand()
    computer_hand = get_hand()


def get_hand() -> list[str]:
    """Return a list representing a player's 4-card hand."""
    deck = []
    while len(deck) < 10:
        value = str(randint(1, 6))
        mod = choice(['+', '-', '±'])
        card = mod + value
        if deck.count(card) == 2:
            continue
        deck.append(card)

    hand = []
    for _ in range(4):
        shuffle(deck)
        card = deck.pop()
        hand.append(card)
    return hand


def get_house_deck() -> list[str]:
    """Return a list representing the 40-card house deck."""

    deck = []
    for i in range(10):
        for _ in range(4):
            deck.append(str(i + 1))
    return deck


if __name__ == '__main__':
    main()
