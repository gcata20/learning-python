from datetime import datetime
from tabulate import tabulate
import os
import re
import sqlite3
import sys


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
            name_error = 'Contact creation failed. Must provide a name.'
            raise ValueError(name_error)
        self._name = name

    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, email) -> None:
        email_pattern = r'[0-9a-zA-Z_\-\.]+@[^@]+'
        if email and not re.fullmatch(email_pattern, email):
            email_error = 'Contact creation failed. Email not valid.'
            raise ValueError(email_error)
        self._email = email
    
    @property
    def birthday(self) -> str:
        return self._birthday
    
    @birthday.setter
    def birthday(self, birthday) -> None:
        bday_pattern = r'\d{4}(?:-\d{2}){2}'
        if birthday:
            if not re.fullmatch(bday_pattern, birthday):
                invalid_error = 'Contact creation failed. Invalid birthday input.'
                raise ValueError(invalid_error)
            year, month, day = map(int, birthday.split('-'))
            try:
                datetime(year, month, day)
            except ValueError:
                inexistent_error = 'Contact creation failed. Birthday date does not exist.'
                raise ValueError(inexistent_error)
        self._birthday = birthday

    def get_details(self):
        return [self._name, self._email, self.phone, self._birthday, self.note]
    
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
            print(f'[Error]: {err}')


def main():
    db = db_init()
    main_menu(db)


# Custom functions.
def db_init() -> str:
    """Initializes a database file and returns it."""

    db = 'data.db'
    if not os.path.exists(db):
        init_query = """
            CREATE TABLE contacts (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE COLLATE NOCASE,
                email TEXT,
                phone TEXT,
                birthday TEXT,
                note TEXT
            )
        """
        db_query(db, init_query)
    return db


def db_query(db: str, query: str, *values, fetch=''):
    """
    Performs all db interactions:
    - opens a connection and creates a cursor
    - executes a query (with values if provided) and catches errors
    - commits any transactions where necessary
    - closes the cursor and connection
    - (optional) may return data using the fetch parameter:
        - 'all': calls cursor.fetchall() and saves result as a list of dicts
        - 'one': calls cursor.fetchone() and saves result as a dict
        - '': default, does nothing
        - any other value will raise a SyntaxError
    """

    result = None
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(query, values)
    except sqlite3.IntegrityError as e:
        integrity_error = str(e)
        if integrity_error == 'UNIQUE constraint failed: contacts.name':
            unique_name_error = '[Error]: A contact with that name already exists.'
            print(unique_name_error)
    else:
        if any(word in query for word in ['CREATE', 'INSERT', 'UPDATE', 'DELETE']):
            conn.commit()
        match fetch.strip().lower():
            case 'all':
                if fetched_rows := cursor.fetchall():
                    result = [dict(row) for row in fetched_rows]
            case 'one':
                if fetched_row := cursor.fetchone():
                    result = dict(fetched_row)
            case '':
                pass
            case _:
                fetch_error = 'Wrong use of the db_query fetch parameter.'
                raise SyntaxError(fetch_error)
    finally:
        cursor.close()
        conn.close()
    return result


def main_menu(db: str):
    """Main menu loop for accessing the app's main features."""

    show_options('main')

    while True:
        match input('-> ').strip().lower():
            case '1':
                all_query = """
                    SELECT name, email, phone, birthday, note
                    FROM contacts
                    ORDER BY LOWER (name)
                """
                if results := db_query(db, all_query, fetch='all'):
                    print(tab(results))
                else:
                    no_contacts_msg = 'Database is empty. Get started by creating a new contact.'
                    print(no_contacts_msg)
            case '2':
                search = '%' + input('Search for: ').strip().lower() + '%'
                matching_query = """
                    SELECT name, email, phone, birthday, note
                    FROM contacts
                    WHERE LOWER (name) LIKE ?
                    ORDER BY LOWER (name)
                """
                if results := db_query(db, matching_query, search, fetch='all'):
                    print(tab(results))
                else:
                    no_matches_msg = 'No matches found.'
                    print(no_matches_msg)
            case '3':
                new_contact = Contact.get()
                if new_contact:
                    create_query = """
                        INSERT INTO contacts (name, email, phone, birthday, note)
                        VALUES (?, ?, ?, ?, ?)
                    """
                    db_query(db, create_query, *new_contact.get_details())
                        
            case '4':
                #TODO: Modify existing contact by calling mod menu with contact id.
                ...
            case 'm':
                show_options('main')
            case 'x':
                print('Adios.')
                sys.exit(0)
            case _:
                invalid_choice_msg = 'Invalid choice. Type m to show main menu options.'
                print(invalid_choice_msg)


def mod_menu(db: str, id: str):
    """Mod menu loop for modifying contact details."""

    show_options('mod')

    while True:
        match input('-> ').strip().lower():
            case '1':
                #TODO: Show contact's current status.
                ...
            case '2':
                #TODO: Change contact's name.
                ...
            case '3':
                #TODO: Change contact's email.
                ...
            case '4':
                #TODO: Change contact's phone number.
                ...
            case '5':
                #TODO: Change contact's birthday.
                ...
            case '6':
                #TODO: CHange contact's note.
                ...
            case '7':
                #TODO: Delete contact.
                ...
            case '8':
                #TODO: Go back to the main menu.
                ...
            case 'm':
                show_options('mod')
            case 'x':
                print('Adios.')
                sys.exit(0)
            case _:
                invalid_choice_msg = 'Invalid choice. Type m to show modify menu options.'
                print(invalid_choice_msg)


def show_options(menu: str):
    """
    Prints a text-based UI menu with options.
    
    Choices for the menu parameter:
    - 'main' = main menu
    - 'mod' = modify contact menu
    - any other value will raise a SyntaxError
    """

    if menu == 'main':
        print(
            '───── [ Main Menu ] ─────\n'
            '[1] Show All Contacts\n'
            '[2] Search for Contact(s)\n'
            '[3] Create New Contact\n'
            '[4] Modify Contact\n'
            '[x] Exit'
        )
    elif menu == 'mod':
        print(
            '───── [ Modify Contact Menu ] ─────\n'
            '[1] Show Current Status\n'
            '[2] Change Name\n'
            '[3] Change Email\n'
            '[4] Change Phone Number\n'
            '[5] Change Birthday'
            '[6] Change Note'
            '[7] Delete Contact\n'
            '[8] Back to Main Menu\n'
            '[x] Exit'
        )
    else:
        error_msg = 'Invalid use of the show_options menu parameter.'
        raise SyntaxError(error_msg)


def tab(data: list[dict]):
    """Uses the tabulate module to return a table-like string for printing."""

    return tabulate(data, headers='keys', tablefmt='simple_grid')


if __name__ == '__main__':
    main()
