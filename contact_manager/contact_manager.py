from tabulate import tabulate
import re


class Contact:
    def __init__(self, name, email='', phone='', birthday='', note='') -> None:
        self.name = name
        self.email = email
        self.phone = phone
        self.birthday = birthday
        self.note = note
    
    def __str__(self) -> str:
        s = tabulate([self.__dict__], headers='keys', tablefmt='simple_grid')
        return s
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name) -> None:
        if not name:
            raise ValueError('Contact creation failed. Must provide a name.')
        self._name = name

    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, email) -> None:
        pattern = r'[0-9a-zA-Z_\-\.]+@[^@]+'
        if email and not re.fullmatch(pattern, email):
            raise ValueError('Contact creation failed. Email not valid.')
        self._email = email
    
    @property
    def birthday(self) -> str:
        return self._birthday
    
    @birthday.setter
    def birthday(self, birthday) -> None:
        pattern = r'\d{4}(?:-\d){2}'
        if birthday and not re.fullmatch(pattern, birthday):
            raise ValueError('Contact creation failed. Birthday not valid.')
        self._birthday = birthday
    
    @classmethod
    def get(cls):
        """Returns a new Contact object, initialized from user input."""

        name = input('Name: ').strip()
        email = input('Email: ').strip()
        phone = input('Phone: ').strip()
        birthday = input('Birthday (YYYY-MM-DD): ').strip()
        note = input('Note: ').strip()
        try:
            return cls(name, email, phone, birthday, note)
        except ValueError as err:
            print(err)


def main():
    new_contact = Contact.get()
    print(f'[Contact details]:\n{new_contact}')


if __name__ == '__main__':
    main()
