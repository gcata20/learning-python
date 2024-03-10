from tabulate import tabulate
import json
import re


class Contact:
    def __init__(self, name, email="", phone="", birthday="", note="") -> None:
        self.name = name
        self.email = email
        self.phone = phone
        self.birthday = birthday
        self.note = note
    
    def __str__(self) -> str:
        s = tabulate([self.__dict__], headers="keys", tablefmt="simple_grid")
        return s
    
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
        pattern = r'[0-9a-zA-Z_\-\.]+@[^@]+'
        if not re.fullmatch(pattern, email):
            raise ValueError('Creation failed. Email not valid.')
        self._email = email
    
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
    # input_contacts = [
    #     Contact('contact_1', 'name-1@fake-domain'),
    #     Contact('contact_2', 'name-2@fake-domain', '0565146935'),
    #     Contact('contact_3', 'name-3@fake-domain', '', '05-11-1956'),
    #     Contact('contact_4', 'name-4@fake-domain', '', '', 'This is a note.')
    # ]
    # contacts_to_write = [con.__dict__ for con in input_contacts]
    # with open('contacts.json', 'w') as f:
    #     json.dump(contacts_to_write, f, indent=4)
    ...


if __name__ == '__main__':
    main()
