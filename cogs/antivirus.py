import discord
from discord.ext import commands
import asyncio
import io

from bot import AutoVulnBot, Scanner


class Antivirus(commands.Cog):
    def __init__(self, bot: AutoVulnBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ctx = await self.bot.get_context(message)
        flag = 0
        m = f"Message ID: {message.id} has been flagged for containing malicious content:\n"
        for attachment in message.attachments:
            flag = 0
            stream = io.BytesIO()
            await attachment.save(stream)
            stream.seek(0)
            data = stream.read()
            stream.seek(0)
            results = self.bot.scanner.scanfobj(stream)
            if not results:
                continue
            flag = 1
            for result in results:
                m += f"Attachment {attachment.id} was flagged for matching {result}\n\n"
            if flag:
                await ctx.send(m)
                await ctx.send("Here is a permanent link to the file if "
                               "you want to check maliciousness: "
                               f"{await self.bot.paste_gg_post(data, attachment.filename)}")
                await ctx.send(f"The original filename is {attachment.filename} if you would like to recreate it.")
        if flag:
            await ctx.send("The message will be deleted in 15 seconds.")
            await asyncio.sleep(15)
            await message.delete()

    @commands.command(aliases=["reloadrules", "reloadscanner"])
    @commands.is_owner()
    async def reloadconf(self, ctx: commands.context.Context):
        self.bot.scanner = Scanner()
        await ctx.send("Reloaded SCANNER")


def setup(bot):
    bot.add_cog(Antivirus(bot))
