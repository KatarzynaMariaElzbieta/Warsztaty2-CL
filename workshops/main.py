from models import User
import argparse
from clcrypto import check_password
from database import get_connection, get_cursor

parser = argparse.ArgumentParser(description="Opis naszej aplikacji")

parser.add_argument('-u', '--user', type=str, help="Pomoc komendy. Użycie -u login")
parser.add_argument('-p', '--password', type=str, help="Pomoc komendy. Użycie -p hasło")
parser.add_argument('-n', '--new_pass', type=str, help="Pomoc komendy. Użycie -n nowe hasło")
parser.add_argument('-l', '--list', type=str, help="Pomoc komendy. Użycie -l", required=False, default="")
parser.add_argument('-d', '--delete', type=str, help="Pomoc komendy. Użycie -d login użytkownika do usunięcia")
parser.add_argument('-e', '--edit', type=str, help="Pomoc komendy. Użycie -n login użytkownka do modyfikacji")

args = parser.parse_args()

if __name__ == '__main__':
    connection = get_connection()
    cursor = get_cursor(connection)
    # Adam = User()
    # Adam.username = "Adam"
    # Adam.email = "adam.pierwszy@wp.pl"
    # Adam.set_password('haslo12')
    # Adam.save_to_db(cursor)
    # print(User.load_user_by_id(cursor, 1).username)
    # print(User.load_user_by_id(cursor, 1).email)

    # zmiana hasła
    if args.user and args.password and args.edit and args.new_pass:
        loaded_user = User.load_user_by_username(cursor, args.user)
        if len(args.new_pass) > 8:
            if loaded_user and check_password(args.password, loaded_user.hashed_password):
                loaded_user.name = args.user
                loaded_user.set_password(args.new_pass)
                loaded_user.save_to_db(cursor)
                print("Hasło zostało zmienione.")
            else:
                print("Błąd z uwierzytelnieniem.")
        else:
            print("Nowe hasło jest za krótkie.")
    # usuwanie użytkownika
    elif args.user and args.password and args.delete:
        loaded_user = User.load_user_by_username(cursor, args.user)
        if check_password:
            loaded_user.delete(cursor)
            print("Użytkownik usunięty")
        else:
            print("Problem z uwierzytelnieniem")
    # logowanie użytkownika lub zakładanie nowego konta
    elif args.user and args.password:
        loaded_user = User.load_user_by_username(cursor, args.user)
        if loaded_user:
            if check_password(args.password, loaded_user.hashed_password):
                print("Zalogowano")
            else:
                print("Nazwa użytkownika i hasło nie pasują do siebie")
        else:
            user = User()
            user.username = args.user
            user.email = args.user
            user.set_password(args.password)
            user.save_to_db(cursor)
    elif args.list:
        all_user = User.load_all_users(cursor)
        for i in all_user:
            print(i.username, i.email)

    connection.close()
