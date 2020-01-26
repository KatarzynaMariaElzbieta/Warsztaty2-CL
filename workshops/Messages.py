from models import User, Message
import argparse
from clcrypto import check_password
from database import get_connection, get_cursor
import datetime

parser = argparse.ArgumentParser(description="Opis naszej aplikacji")

parser.add_argument('-u', '--user', type=str, help="Pomoc komendy. Użycie -u login")
parser.add_argument('-p', '--password', type=str, help="Pomoc komendy. Użycie -p hasło")
parser.add_argument('-l', '--list', type=str, help="Pomoc komendy. Użycie -l lista wiadomości", required=False, default="")
parser.add_argument('-t', '--to', type=str, help="Pomoc komendy. Użycie -t email adresata")
parser.add_argument('-s', '--send', type=str, help="Pomoc komendy. Użycie -s teskt wiadomości do wysłania")

args = parser.parse_args()

if __name__ == '__main__':
    connection = get_connection()
    cursor = get_cursor(connection)
    #
    # message = Message()
    # message.from_id = "11"
    # message.to_id = "9"
    # message.text = "blabla"
    # message.creation_date = datetime.datetime.today()
    # message.save_to_db(cursor)

if args.send and args.user and args.password and args.to and args.send:
    from_user = User.load_user_by_username(cursor, args.user)
    print(from_user.id)
    if from_user and check_password(args.password, from_user.hashed_password):
        to_user = User.load_user_by_email(cursor, args.to)
        if to_user:
            message = Message()
            message.from_id = from_user.id
            message.to_id = to_user.id
            message.text = args.send
            message.creation_date = datetime.datetime.today()
            message.save_to_db(cursor)
            print("Wysłano")
        else:
            print("Błąd. Użytkownik do którego chcesz wysłać wiadomość nie istnieje.")
    else:
        print("Błąd uwierzytelniania")

elif args.list and args.user and args.password:
    loaded_user = User.load_user_by_username(cursor, args.user)
    if loaded_user and check_password(args.password, loaded_user.hashed_password):
        messages = Message.load_all_messages_for_user(cursor, loaded_user.id)
        print("ID: \t Od: \t Treść: \t Data:")
        for m in messages:
            print(m.id, '\t', m.email, '\t', m.text, '\t', m.creation_date)
    else:
        print("Błąd uwierzytelnienia")
elif args.list:
    all_messages = Message.load_all_messages(cursor)
    print("ID: \t Od: \t Do: \t Treść: \t Data:")
    for a in all_messages:
        print(a.id, '\t', a.from_id, '\t', a.to_id, '\t', a.text, '\t', a.creation_date)

    connection.close()
