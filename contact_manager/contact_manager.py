class Contact:
    def __init__(self, name: str, email: str) -> None:
        if not name:
            raise ValueError('Creation failed. Contact must have a name.')
        self.name = name
        self.email = email

    def __str__(self) -> str:
        return f'Contact object associated with the name: {self.name}.'


def main():
    new_contact = get_contact()
    print(new_contact)


def get_contact() -> Contact:
    """Returns a new Contact object, initialized from user input."""

    name = input('Name: ').strip()
    email = input('Email: ').strip()
    try:
        return Contact(name, email)
    except ValueError as err:
        print(err)


if __name__ == '__main__':
    main()