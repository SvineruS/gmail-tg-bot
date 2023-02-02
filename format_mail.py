import email.header
import html
import re

from bs4 import BeautifulSoup

replaces = {
    re.compile(r'( *[\r\n] *){2,}'): '\n',
    re.compile(r' {2,}'): ' ',
    re.compile(r'\s{2,}'): '',
}.items()

trash_tags = ['title', 'style', 'script']


def mail_to_text(mail):
    payload = get_payload(mail)
    text = parse_text_from_payload(payload)

    from_ = mail['from'].split(' <', 1)[0]
    to_ = mail['Delivered-To']

    msg = f"<b>{from_} -> {to_}</b>\n<b>{get_subject(mail)}</b>\n\n{text}"
    if len(msg) > 4096:
        msg = msg[:4096 - 3] + '...'

    return msg


def get_payload(msg):
    if msg.is_multipart():
        return get_payload(msg.get_payload(i=0))

    charset = msg['Content-Type'].split('=')[1].split(';')[0]
    payload = msg.get_payload(decode=True)
    if not payload:
        return ""
    return msg.get_payload(decode=True).decode(charset)


def parse_text_from_payload(payload):
    payload = BeautifulSoup(payload, "html.parser")
    for i in trash_tags:
        for t in payload.findAll(i):
            t.clear()

    payload = payload.text
    for i in replaces:
        payload = i[0].sub(i[1], payload)
    payload = payload.strip()
    payload = html.escape(payload)
    return payload


def get_subject(mail):
    subject, enc = email.header.decode_header(mail['subject'])[0]
    return subject.decode(enc) if enc else subject
