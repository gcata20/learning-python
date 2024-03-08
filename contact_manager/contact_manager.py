import re


class Contact:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

    def __str__(self) -> str:
        return f"""
            Contact object/instance.
            Name: {self._name}
            Email: {self._email}
        """
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name) -> None:
        if not name:
            raise ValueError('Creation failed. Contact must have a name.')
        self._name = name

    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, email) -> None:
        pattern = r'[^@]+@[^@]+'
        if not re.fullmatch(pattern, email):
            raise ValueError('Creation failed. Email not valid.')
        self._email = email
    
    @classmethod
    def get(cls):
        """Returns a new Contact object, initialized from user input."""

        name = input('Name: ').strip()
        email = input('Email: ').strip()
        try:
            return cls(name, email)
        except ValueError as err:
            print(err)


def main():
    new_contact = Contact.get()
    print(new_contact)


if __name__ == '__main__':
    main()
