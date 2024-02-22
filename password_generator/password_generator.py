import secrets
import string


def main():
    psw_len = get_password_length()
    psw = generate_password(psw_len)
    print('Password:', psw)


def get_password_length() -> int:
    while True:
        try:
            len = int(input('Length (8-32): '))
        except ValueError:
            print('Please input a valid number.')
            continue
        if not 7 < len < 33:
            continue
        return len


def generate_password(psw_len: int) -> str:
    chars = string.ascii_letters + string.digits
    psw = ''.join(secrets.choice(chars) for _ in range(psw_len))
    return psw


if __name__ == '__main__':
    main()
