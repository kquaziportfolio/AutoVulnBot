import aiohttp
import discord
from discord.ext.commands import *
from jishaku.help_command import *
import io
import asyncio
import os
import config
import base64 as b64
from scannerlib import yaralib, hasherlib

intents = discord.Intents.all()
print(intents)


class Scanner:
    def __init__(self):
        self.yarascanner = yaralib.YaraScanner()
        self.hashscanner = hasherlib.HashScanner()

    def scanfobj(self, fobj: io.BytesIO):
        d = fobj.read()
        return self.yarascanner.scandata(d) + self.hashscanner.scandata(d)


class AutoVulnBot(Bot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(prefix, *args, **kwargs)
        self.invite = None
        self.scanner = Scanner()
        self.session = aiohttp.ClientSession()

    async def on_connect(self):
        self.session = aiohttp.ClientSession()

    async def on_ready(self):
        self.invite = discord.utils.oauth_url(
            self.user.id, discord.Permissions(permissions=8)
        )
        print(
            "Logged in as",
            client.user.name,
            "\nId:",
            client.user.id,
            "\nOath:",
            self.invite,
        )
        print("--------")

    async def on_message(self, msg: discord.Message):
        # ctx = await self.get_context(msg)
        try:
            await self.process_commands(msg)
        except Exception as err:
            print(err)

    async def paste_gg_post(self, content, n):
        content = b64.b64encode(content).decode()
        async with self.session.post("https://api.paste.gg/v1/pastes", headers={"Content-Type": "application/json"},
                                     data='{"name":"$$$$$name$$$$$","files":[{"name":"$$$$$name$$$$$","content":{'
                                          '"format": "base64","value":"$$$$$value$$$$$"}}]}'
                                          ''.replace("$$$$$value$$$$$", content).replace("$$$$$name$$$$$", n)) as resp:
            out = await resp.json()
        try:
            return "https://paste.gg/" + out["result"]["id"]
        except KeyError:
            return

    async def logout(self):
        await self.session.close()
        await super().logout()

    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    async def process_commands(self, message):
        await super().process_commands(message)

    async def playingstatus(self):
        await self.wait_until_ready()
        while self.is_ready():
            status = "with viruses"
            await self.change_presence(
                activity=discord.Game(name=status), status=discord.Status.online
            )
            await asyncio.sleep(120)


client = AutoVulnBot(
    intents=intents, prefix=when_mentioned_or("avb!"), help_command=DefaultPaginatorHelp()
)
nocogs = []
for file in os.listdir("cogs"):
    if file.endswith(".py") and not (file[:-3] in nocogs):
        name = file[:-3]
        try:
            client.load_extension(f"cogs.{name}")
            print(f"Loaded cog {name}")
        except Exception as e:
            print(f"Failed to load cog {name} due to error\n", e)
client.load_extension("jishaku")
try:
    client.run(config.token)
except:
    print("Bye!")
    raise
