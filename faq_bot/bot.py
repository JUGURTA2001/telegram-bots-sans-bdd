"""Bot FAQ pour un commerce : menu à boutons + recherche libre. Sans base de données."""
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

import config
from faq import best_match

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()


def menu_keyboard() -> InlineKeyboardMarkup:
    """Un bouton par question, plus un bouton Contact."""
    builder = InlineKeyboardBuilder()
    for i, entry in enumerate(config.FAQ):
        builder.button(text=entry["question"], callback_data=f"faq:{i}")
    builder.button(text="📞 Nous contacter", callback_data="contact")
    builder.adjust(1)
    return builder.as_markup()


def back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Retour au menu", callback_data="menu")
    return builder.as_markup()


@dp.message(Command("start", "menu"))
async def cmd_start(message: Message):
    await message.answer(config.WELCOME, reply_markup=menu_keyboard())


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Utilisez /menu pour voir les questions fréquentes, "
        "ou écrivez directement votre question.",
        reply_markup=back_keyboard(),
    )


@dp.callback_query(F.data == "menu")
async def show_menu(callback: CallbackQuery):
    if isinstance(callback.message, Message):
        await callback.message.edit_text(config.WELCOME, reply_markup=menu_keyboard())
    await callback.answer()


@dp.callback_query(F.data == "contact")
async def show_contact(callback: CallbackQuery):
    if isinstance(callback.message, Message):
        await callback.message.edit_text(config.CONTACT, reply_markup=back_keyboard())
    await callback.answer()


@dp.callback_query(F.data.startswith("faq:"))
async def show_answer(callback: CallbackQuery):
    try:
        index = int(callback.data.split(":", 1)[1])
        entry = config.FAQ[index]
    except (ValueError, IndexError):
        await callback.answer("Question introuvable.", show_alert=True)
        return
    if isinstance(callback.message, Message):
        text = f"❓ {entry['question']}\n\n{entry['answer']}"
        await callback.message.edit_text(text, reply_markup=back_keyboard())
    await callback.answer()


@dp.message(F.text)
async def free_text(message: Message):
    """Recherche libre : trouve la question la plus proche du texte reçu."""
    index = best_match(message.text, config.FAQ)
    if index is None:
        await message.answer(config.FALLBACK, reply_markup=menu_keyboard())
        return
    entry = config.FAQ[index]
    await message.answer(
        f"❓ {entry['question']}\n\n{entry['answer']}", reply_markup=back_keyboard()
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    if not TOKEN:
        raise SystemExit("BOT_TOKEN introuvable : vérifiez votre fichier .env")
    bot = Bot(token=TOKEN)
    try:
        await bot.set_my_commands(
            [
                BotCommand(command="menu", description="Afficher les questions"),
                BotCommand(command="help", description="Aide"),
            ]
        )
    except Exception as exc:  # le bot reste utilisable sans le menu de commandes
        logging.warning("Impossible de définir les commandes : %s", exc)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
