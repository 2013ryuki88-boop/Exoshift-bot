import discord
from discord.ext import commands
import datetime
import os

# Botの設定
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.mentions = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} としてログインしました！')
    print('準備完了です。Discordでテストしてみてください。')

# !to コマンド (タイムアウト)
@bot.command(name="to")
@commands.has_permissions(moderate_members=True)
async def timeout_command(ctx, member: discord.Member, minutes: int):
    if not ctx.guild.me.guild_permissions.moderate_members:
        await ctx.send("❌ エラー: Botに「メンバーをタイムアウト」権限がありません。")
        return
    if member == ctx.author or member.bot:
        await ctx.send("❌ 自分自身やBotをタイムアウトすることはできません。")
        return
    try:
        duration = datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=f"{ctx.author.name} によるタイムアウト")
        await ctx.send(f"🔇 {member.mention} を **{minutes}分間** タイムアウトしました。")
    except Exception as e:
        await ctx.send(f"❌ タイムアウトに失敗しました。\n理由: {e}")

@timeout_command.error
async def timeout_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ あなたにはこのコマンドを実行する権限がありません。")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ 使い方: `!to @ユーザー 10`")

# !kick コマンド (キック)
@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, member: discord.Member):
    if not ctx.guild.me.guild_permissions.kick_members:
        await ctx.send("❌ エラー: Botに「メンバーをキック」権限がありません。")
        return
    if member == ctx.author or member.bot:
        await ctx.send("❌ 自分自身やBotをキックすることはできません。")
        return
    try:
        await member.kick(reason=f"{ctx.author.name} によるキック")
        await ctx.send(f"👢 {member.name} をキックしました。")
    except Exception as e:
        await ctx.send(f"❌ キックに失敗しました。\n理由: {e}")

@kick_command.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ あなたにはこのコマンドを実行する権限がありません。")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ 使い方: `!kick @ユーザー`")

# ==========================================
# Renderの環境変数からトークンを読み込んで起動
# ==========================================
bot.run(os.getenv('DISCORD_TOKEN'))
