import argparse

from psycopg2 import connect, OperationalError

from clcrypto import check_password
from models import User, Messages
import create_db

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all messages", action="store_true")
parser.add_argument("-t", "--to", help="to")
parser.add_argument("-s", "--send", help="text message to send")

args = parser.parse_args()


def print_user_messages(cursor, user):
    messages = Messages.load_all_messages(cursor, user.id)
    for message in messages:
        from_ = User.load_user_by_id(cursor, message.from_id)
        print(20 * "-")
        print(f"from: {from_.username}")
        print(f"data: {message.creation_date}")
        print(message.text)
        print(20 * "-")


def send_message(cursor, from_id, recipient_name, text):
    if len(text) > 255:
        print("Message is too long!")
        return
    to = User.load_user_by_username(cursor, recipient_name)
    if to:
        message = Messages(from_id, to.id, text=text)
        message.save_to_db(cursor)
        print("Message send")
    else:
        print("Recipient does not exist.")


if __name__ == '__main__':
    try:
        con = connect(database="workshop", user=create_db.DB_USER, password=create_db.PASSWORD, host=create_db.HOST)
        con.autocommit = True
        cursor = con.cursor()
        if args.username and args.password:
            user = User.load_user_by_username(cursor, args.username)
            if check_password(args.password, user.hashed_password):
                if args.list:
                    print_user_messages(cursor, user)
                elif args.to and args.send:
                    send_message(cursor, user.id, args.to, args.send)
                else:
                    parser.print_help()
            else:
                print("Incorrect password or User does not exists!")
        else:
            print("username and password are required")
            parser.print_help()
        con.close()
    except OperationalError as err:
        print("Connection Error: ", err)
