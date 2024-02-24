import secrets
import string
import sys


MIN = 8
MAX = 32


def main():
    while True:
        psw_len = get_password_length()
        psw = generate_password(psw_len)
        print('Password:', psw)

        while True:
            user_input = input('Generate another password? (y/n): ').strip().lower()
            if user_input == 'y':
                break
            elif user_input == 'n':
                sys.exit(0)


def get_password_length() -> int:
    while True:
        try:
            len = int(input(f'Length ({MIN}-{MAX}): '))
        except ValueError:
            print('Please input a valid number.')
            continue
        if not MIN <= len <= MAX:
            continue
        return len


def generate_password(psw_len: int) -> str:
    chars = string.ascii_letters + string.digits
    psw = ''.join(secrets.choice(chars) for _ in range(psw_len))
    return psw


if __name__ == '__main__':
    main()
