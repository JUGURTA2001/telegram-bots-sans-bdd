"""Bot de contact : relaie les messages des clients vers le propriétaire, et ses réponses
vers les clients. Sans base de données (voir relay.py pour l'astuce utilisée)."""
import asyncio
import logging
import os
import time

from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError
from aiogram.filters import Command
from aiogram.types import BotCommand, Message
from dotenv import load_dotenv

from relay import RateLimiter, build_forward, extract_user_id, is_too_long

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", ""))
except ValueError:
    ADMIN_ID = 0

dp = Dispatcher()
limiter = RateLimiter(delay=2.0)

USER_WELCOME = (
    "👋 Bonjour ! Écrivez votre message ici : je le transmets à l'équipe, "
    "qui vous répondra dès que possible."
)
ADMIN_HELP = (
    "👑 Mode administrateur.\n\n"
    "Les messages des clients arrivent ici. Pour répondre, utilisez la fonction "
    "« Répondre » (Reply) de Telegram sur le message du client : ma réponse lui sera envoyée."
)


@dp.message(Command("start", "help"))
async def cmd_start(message: Message):
    is_admin = message.from_user and message.from_user.id == ADMIN_ID
    await message.answer(ADMIN_HELP if is_admin else USER_WELCOME)


# --- Côté administrateur -------------------------------------------------------

@dp.message(F.from_user.id == ADMIN_ID, F.reply_to_message)
async def admin_reply(message: Message):
    user_id = extract_user_id(message.reply_to_message.text)
    if user_id is None:
        await message.answer("⚠️ Répondez à un message de client (celui qui contient [ID:...]).")
        return
    if not message.text:
        await message.answer("⚠️ Seules les réponses en texte sont prises en charge.")
        return
    try:
        await message.bot.send_message(user_id, f"💬 Réponse de l'équipe :\n\n{message.text}")
    except TelegramForbiddenError:
        await message.answer("⚠️ Ce client a bloqué le bot : réponse non envoyée.")
    except TelegramAPIError as exc:
        await message.answer(f"⚠️ Envoi impossible : {exc}")
    else:
        await message.answer("✅ Réponse envoyée.")


@dp.message(F.from_user.id == ADMIN_ID)
async def admin_other(message: Message):
    await message.answer(ADMIN_HELP)


# --- Côté client ------------------------------------------------------------------

@dp.message(F.text)
async def user_message(message: Message):
    if not limiter.allow(message.from_user.id, time.monotonic()):
        await message.answer("⏳ Merci de patienter quelques secondes entre deux messages.")
        return
    if is_too_long(message.text):
        await message.answer("⚠️ Message trop long. Merci de le raccourcir.")
        return
    user = message.from_user
    forward = build_forward(user.id, user.full_name, user.username, message.text)
    try:
        await message.bot.send_message(ADMIN_ID, forward)
    except TelegramAPIError:
        logging.exception("Impossible de joindre l'administrateur")
        await message.answer("⚠️ Désolé, le message n'a pas pu être transmis. Réessayez plus tard.")
        return
    await message.answer("✅ Message envoyé. Nous vous répondrons bientôt.")


@dp.message()
async def unsupported(message: Message):
    await message.answer("Seuls les messages texte sont pris en charge pour l'instant.")


async def main():
    logging.basicConfig(level=logging.INFO)
    if not TOKEN:
        raise SystemExit("BOT_TOKEN introuvable : vérifiez votre fichier .env")
    if not ADMIN_ID:
        raise SystemExit("ADMIN_ID introuvable ou invalide : voir .env.example")
    bot = Bot(token=TOKEN)
    try:
        await bot.set_my_commands(
            [BotCommand(command="start", description="Écrire à l'équipe")]
        )
    except Exception as exc:
        logging.warning("Impossible de définir les commandes : %s", exc)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
