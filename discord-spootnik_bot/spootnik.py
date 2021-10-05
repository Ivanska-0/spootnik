import os
import re

import discord

from discord import Game
from support import extract, get_term_clock_pid, check_alive

from signal import SIGUSR1, SIGTERM
from random import randrange
from discord.ext import commands
from dotenv import load_dotenv
from time import sleep

from random_facts import random_fact

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise(FileNotFoundError)

bot = commands.Bot(command_prefix="--", help_command=None)


@bot.command()
async def alive(ctx):
    if check_alive():
        await ctx.send("El servidor de Minecraft está operativo, mi pana.")
    else:
        await ctx.send("El servidor de Minecraft está jodío, mi pana.")


@bot.command()
@commands.has_role("MAINCRAA")
async def extend(ctx):
    if not check_alive():
        await ctx.send("El servidor de Minecraft está jodío, mi pana.")
    else:
        pid = get_term_clock_pid()
        os.kill(pid, SIGUSR1)
        await ctx.send("Vuestras plegarias han sido escuchadas. Cerrando el servidor de Minecraft en 30 minutos.")


@bot.command()
@commands.has_role("MAINCRAA")
async def stop(ctx):
    if not check_alive():
        await ctx.send("El servidor de Minecraft está jodío, mi pana.")
    else:
        pid = get_term_clock_pid()
        os.kill(pid, SIGTERM)
        await ctx.send("Servidor de Minecraft cerrándose. Buenas noches.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

    if randrange(50) == 1:
        await message.channel.send("Hey, {0.author.mention}, did you know that ".format(message) + random_fact())

    if message.content == "a.":
        if randrange(20) == 13:
            await message.channel.send("Papopepoparapapapapa")

        else:
            await message.channel.send("a.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("ESE COMANDO. NO PODÉS.\n\n(no tienes el rol adecuado).")


@bot.event
async def on_ready():
    await bot.change_presence(activity=Game(name="--help"))
    print("Spootnik launched.")


@bot.command()
async def help(ctx):
    await ctx.send("Pootin estará esperando en tus MDs...")
    await ctx.author.create_dm()
    await ctx.author.dm_channel.send(
        f"**PAPOPEPOPARAPAPAPAPA**\n"
        "**Spootnik Bot (no copyrighterino de la Unión Soviética) para asistir al servidor Sputnik**\n\n"
        "De momento las funcionalidades implementadas son:\n"
        "* Si escribes \"a.\" te responderé igual (¡con un pequeño porcentaje de un *easter egg*!)\n"
        "* Con una pequeña probabilidad, por cada mensaje en el servidor que lea, escribiré una curiosidad random que seguramente no necesitabas.\n\n"
        "**Comandos**\n"
        "--alive\t\t\t\tComprueba si el servidor de Minecraft está vivo.\n"
        "--extend\t\t\tFija la hora de cierre del servidor a dentro de 30 minutos. Útil para extender su tiempo.\n"
        "--stop\t\t\t\tCierra el servidor de Minecraft.\n"
        "\n"
        "Y ya está, que mi creador probablemente esté estudiando la engenería o procrastinando.\n"
        "*Bot still work-in-progress*\n\n"
        "Ivanska " u"\U0001F12F" " 2021, All rights *reversed*"
    )


bot.run(TOKEN)
