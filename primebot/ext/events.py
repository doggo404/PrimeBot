import discord
import primebot
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as ---->', self.bot.user, 'ID:', self.bot.user.id)
        await self.bot.change_presence(activity=discord.Game(name=">help | {} servers".format(len(self.bot.guilds))))

    @commands.Cog.listener()
    async def on_command(self, ctx):
        logChannel = self.bot.get_channel(primebot.conf['log']['log_channel'])
        await logChannel.send('Message Author: {}\nMessage Content: {}\nLocation: {} # {}\n\n'.format(ctx.message.author, ctx.message.content, ctx.message.guild.name, ctx.message.channel.name))
        new = {
            "author": str(ctx.message.author),
            "content": str(ctx.message.content),
            "location": ctx.message.guild.name + "#" + ctx.message.channel.name
        }
        primebot.db.executed.insert_one(new)
        with open('log.txt', 'a') as log:
            log.write('Message Author: {}\nMessage Content: {}\nLocation: {} # {}\n\n'.format(ctx.message.author, ctx.message.content, ctx.message.guild.name, ctx.message.channel.name))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if 'happy birthday' in message.content.lower():
            await message.channel.send('Happy Birthday! 🎈🎉')
        if 'i want to die' in message.content.lower():
            await message.channel.send("Are you considering suicide? You are not alone. If you feel suicidal, please call the suicide prevention hotline at 800-273-8255.")

        if message.content == '<@!788810436535386112>' or message.content == '<@788810436535386112>':
            await message.channel.send("Prefix is {}".format(primebot.db.prefixes.find_one({"guild_id": message.guild.id})['prefix']))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(description=f"Joined guild {guild.name} [{guild.id}]")
        embed.set_thumbnail(url=guild.icon_url_as(static_format="png"))
        embed.add_field(
            name="**Members**",  # Basic stats about the guild
            value=f"**Total:** {len(guild.members)}\n" + f"**Admins:** {len([m for m in guild.members if m.guild_permissions.administrator])}\n" + f"**Owner: ** {guild.owner}\n", inline=False)
        guildChannel = self.bot.get_channel(primebot.conf['log']['guild_notifs'])
        await guildChannel.send(embed=embed)
        guild_id = guild.id
        primebot.db.prefixes.delete_one({'guild_id': guild_id})

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(description=f"Removed from guild {guild.name} [{guild.id}]")
        embed.set_thumbnail(url=guild.icon_url_as(static_format="png"))
        guildChannel = self.bot.get_channel(primebot.conf['log']['guild_notifs'])
        await guildChannel.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
