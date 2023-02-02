import asyncio
import logging

from aiogram import Bot

import config
import format_mail
import receive_mail

bot = Bot(token=config.TOKEN, parse_mode="HTML")


async def check_mail(username, password):
    try:
        conn = receive_mail.get_conn(username, password)
        for m in receive_mail.receive_mail(conn):
            await bot.send_message(config.TG_RECEIVER, format_mail.mail_to_text(m))
            logging.info(f"Sent message from {username} mailbox")
            await asyncio.sleep(1.5)
    except Exception as ex:
        try:
            logging.exception("check_mails")
            await bot.send_message(config.TG_RECEIVER, f"{username} exception: \n{str(ex)}")
        except:
            logging.exception(f"Failed to send message to user {config.TG_RECEIVER}")
        return


async def check_daemon(timeout):
    while True:
        try:
            for username, password in config.MAIL_BOXES:
                await check_mail(username, password)
        except Exception as ex:
            logging.exception("check_daemon")
        await asyncio.sleep(timeout)


if __name__ == '__main__':
    asyncio.run(check_daemon(60))


