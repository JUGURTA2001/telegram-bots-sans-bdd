"""Bot convertisseur : unités (hors ligne) et devises (API publique). Sans base de données."""
import asyncio
import logging
import os
import time

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import BotCommand, Message
from dotenv import load_dotenv

from converter import ConversionError, answer, format_number, parse_currency, units_help

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

RATES_URL = "https://open.er-api.com/v6/latest/{base}"
CACHE_SECONDS = 3600  # 1 h : respecte l'API gratuite et évite les appels inutiles
ATTRIBUTION = "Taux : exchangerate-api.com (mis à jour une fois par jour)"

# Cache en mémoire (disparaît à l'arrêt du bot) : pas de base de données nécessaire.
_rates_cache: dict[str, tuple[float, dict[str, float]]] = {}

dp = Dispatcher()

START_TEXT = (
    "👋 Je suis un convertisseur.\n\n"
    "Unités : écrivez par exemple\n"
    "• 10 km en mi\n"
    "• 70 kg en lb\n"
    "• 25 c en f\n\n"
    "Devises : /devise 100 EUR USD\n"
    "Liste des unités : /unites"
)


async def get_rates(base: str) -> dict[str, float]:
    """Récupère les taux de change pour `base`, avec cache d'une heure."""
    cached = _rates_cache.get(base)
    if cached and time.monotonic() - cached[0] < CACHE_SECONDS:
        return cached[1]
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(RATES_URL.format(base=base)) as resp:
            data = await resp.json(content_type=None)
    if data.get("result") != "success":
        raise ConversionError(f"Devise inconnue ou indisponible : {base}.")
    rates = data["rates"]
    _rates_cache[base] = (time.monotonic(), rates)
    return rates


@dp.message(Command("start", "help"))
async def cmd_start(message: Message):
    await message.answer(START_TEXT)


@dp.message(Command("unites"))
async def cmd_units(message: Message):
    await message.answer(units_help())


@dp.message(Command("devise", "currency"))
async def cmd_currency(message: Message, command: CommandObject):
    try:
        amount, src, dst = parse_currency(command.args or "")
        rates = await get_rates(src)
        if dst not in rates:
            raise ConversionError(f"Devise inconnue : {dst}.")
        result = amount * rates[dst]
    except ConversionError as exc:
        await message.answer(f"⚠️ {exc}")
        return
    except (aiohttp.ClientError, asyncio.TimeoutError):
        await message.answer("⚠️ Service de taux indisponible, réessayez dans un instant.")
        return
    await message.answer(
        f"💱 {format_number(amount)} {src} = {format_number(result)} {dst}\n\n{ATTRIBUTION}"
    )


@dp.message(F.text)
async def free_text(message: Message):
    """Toute autre ligne de texte est traitée comme une conversion d'unités."""
    try:
        await message.answer(f"✅ {answer(message.text)}")
    except ConversionError as exc:
        await message.answer(f"⚠️ {exc}")


async def main():
    logging.basicConfig(level=logging.INFO)
    if not TOKEN:
        raise SystemExit("BOT_TOKEN introuvable : vérifiez votre fichier .env")
    bot = Bot(token=TOKEN)
    try:
        await bot.set_my_commands(
            [
                BotCommand(command="devise", description="Convertir des devises"),
                BotCommand(command="unites", description="Liste des unités"),
                BotCommand(command="help", description="Aide"),
            ]
        )
    except Exception as exc:
        logging.warning("Impossible de définir les commandes : %s", exc)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
