from tabulate import tabulate
import os
import re
import sqlite3


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
        if birthday and not re.fullmatch(bday_pattern, birthday):
            bday_msg = 'Contact creation failed. Birthday not valid.'
            raise ValueError(bday_msg)
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
            print(f'[Error] {err}')


def main():
    # db = db_init()
    new_contact = Contact.get()

    # print(
    #     '[Contact details]:\n'
    #     f'{new_contact}'
    # )

    # add_query = """
    #     INSERT INTO contacts (name, email, phone, birthday, note)
    #     VALUES (?, ?, ?, ?, ?)
    # """
    # add_values = [
    #     new_contact.name,
    #     new_contact.email,
    #     new_contact.phone,
    #     new_contact.birthday,
    #     new_contact.note
    # ]
    # db_query(db, add_query, *add_values)

    # q = 'SELECT * FROM contacts WHERE name = ?'
    # name = 'cow'
    # row = db_query(db, q, name, fetch='one')
    # print(row)
    # print(tabulate([row], headers='keys', tablefmt='simple_grid'))


# Custom functions.
def db_init() -> str:
    """Initializes a database file and returns it."""

    db = 'data.db'
    if not os.path.exists(db):
        init_query = """
            CREATE TABLE contacts (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
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
    - executes a query (with values if provided) and cathches errors
    - commits any transactions where necessary
    - closes the cursor and connection
    - (optional) may return data using the fetch parameter:
        - 'all': calls cursor.fetchall() and saves result as a list of dicts
        - 'one': calls cursor.fetchone() and saves result as a dict
    """

    result = None
    try:
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, values)
    except sqlite3.Error as err:
        #TODO: Handle situations like when the user tried to create a contact with a name that exists already.
        print('[DEBUG LOG (ERROR)]:', err)
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
    finally:
        cursor.close()
        conn.close()
        return result


if __name__ == '__main__':
    main()
