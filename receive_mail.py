import email.header
import imaplib


def get_conn(user, password, host='imap.gmail.com', port=993):
    try:
        conn = imaplib.IMAP4_SSL(host, port)
        conn.login(user, password)
        return conn
    except Exception as ex:
        raise Exception(f"Failed to connect to account {user}: {ex}") from ex


def receive_mail(conn):
    conn.select('INBOX', False)
    _, inbox = conn.search(None, 'UNSEEN')

    for num in inbox[0].split():
        _, data = conn.fetch(num, '(RFC822)')
        yield email.message_from_bytes(data[0][1])
        conn.store(num, '+FLAGS', r'\Seen')
