import discord
from discord.ext import commands, tasks
import random
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
QUOTES_CHANNEL_ID = int(os.getenv("QUOTES_CHANNEL_ID", "0"))
QUOTE_TIME = os.getenv("QUOTE_TIME", "12:00")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

CHARACTERS = {
    "Charlie": {"color": 0xCC0000, "gifs": ["https://media.tenor.com/F1N1I6lhr4AAAAC/charlie-morningstar-hazbin-hotel.gif", "https://media.tenor.com/7nQ9XQjXxQAAAAC/charlie-hazbin.gif", "https://media.tenor.com/KjqBc-XJwIoAAAAC/charlie-morningstar-hazbin-hotel.gif"], "quotes": ["Every soul deserves a second chance! That's what the hotel is all about!", "Redemption isn't just possible — it's inevitable if you believe in yourself!", "We're gonna save every soul in Hell, one hug at a time!", "I believe in you! I believe in all of you!", "If we can change just one heart, it's all worth it!", "Dream big, work hard, and never give up on anyone!", "The Hazbin Hotel isn't just a building — it's a family!", "You can't spell 'redemption' without 'determination'!"]},
    "Vaggie": {"color": 0x9B59B6, "gifs": ["https://media.tenor.com/5dF5m5e5X5AAAAAC/vaggie-hazbin.gif", "https://media.tenor.com/KmX5n5e5X5AAAAAC/vaggie-hazbin-hotel.gif", "https://media.tenor.com/R5m5e5X5dF5AAAAAC/vaggie-angry.gif"], "quotes": ["I will protect this hotel and everyone in it. Try me.", "Trust is earned. And you're not there yet.", "I've killed angels. A mortal sinner is nothing.", "Charlie believes in you. That's good enough for me.", "One wrong move and you'll answer to my spear.", "The hotel has rules for a reason. Follow them.", "You think this is a joke? People's souls are at stake.", "I didn't survive the extermination just to watch you mess this up."]},
    "Angel Dust": {"color": 0xFF69B4, "gifs": ["https://media.tenor.com/6dF6m6e6X6AAAAAC/angel-dust-hazbin.gif", "https://media.tenor.com/LmX6n6e6X6AAAAAC/angel-dust-hazbin-hotel.gif", "https://media.tenor.com/S6m6e6X6dF6AAAAAC/angel-dust.gif"], "quotes": ["Ugh, Monday am I right? Oh wait, time doesn't exist here!", "I'm not a slut, I'm a high-class escort. There's a difference, sweetheart.", "If I can be redeemed, literally anyone can. I'm a disaster.", "The only thing harder than my life is... well, a lot of things, baby.", "Charlie's optimism is honestly exhausting. But kinda cute.", "I don't do mornings. Or afternoons. Or really any time before noon.", "Trust me, I've done things that would make you blush. And I enjoyed them.", "You're staring. I don't blame you. I'm a masterpiece."]},
    "Alastor": {"color": 0x8B0000, "gifs": ["https://media.tenor.com/8dF8m8e8X8AAAAAC/alastor-hazbin.gif", "https://media.tenor.com/NmX8n8e8X8AAAAAC/alastor-hazbin-hotel.gif", "https://media.tenor.com/T8m8e8X8dF8AAAAAC/alastor-radio-demon.gif"], "quotes": ["I'm not here to make friends. I'm here for the entertainment!", "There is nothing quite like the sound of a sinner's scream over the radio waves!", "I could have taken over Hell myself, but where's the fun in that?", "The hotel is my little pet project. Don't touch what's mine.", "Why be a king when you can be a star?", "I've made a deal with every overlord in Hell. Some of them even survived.", "Static is such a wonderful sound, don't you think?", "I'm the Radio Demon, darling! Did you expect anything less than spectacular?"]},
    "Cherri Bomb": {"color": 0xFF4500, "gifs": ["https://media.tenor.com/9dF9m9e9X9AAAAAC/cherri-bomb-hazbin.gif", "https://media.tenor.com/OmX9n9e9X9AAAAAC/cherri-bomb.gif", "https://media.tenor.com/U9m9e9X9dF9AAAAAC/cherri-bomb-hazbin-hotel.gif"], "quotes": ["I didn't survive this long in Hell by playing nice!", "Bombs are my love language. What's yours?", "Angel's my bestie. Mess with him and I'll blow your ass to the next circle!", "Rules? Where we're going, we don't need rules!", "I lost my eye to an angel. Worth it though.", "Hell is what you make it. I made it EXPLOSIVE!", "You think that's crazy? You should see me on a Tuesday.", "I don't do redemption. I do destruction. There's a difference!"]},
    "Niffty": {"color": 0xFF1493, "gifs": ["https://media.tenor.com/0dF0m0e0X0AAAAAC/niffty-hazbin.gif", "https://media.tenor.com/PmX0n0e0X0AAAAAC/niffty-hazbin-hotel.gif", "https://media.tenor.com/V0m0e0X0dF0AAAAAC/niffty.gif"], "quotes": ["I like bad boys! Especially stabby ones!", "Cleanliness is next to godliness! And we're in Hell, so...", "STAB STAB STAB! Oh sorry, got carried away!", "Men are trash. Literally. I take out the trash.", "I'm just a little demon with big dreams and a bigger knife!", "You're so tall! Can I climb you?", "Killed my husband! He deserved it though.", "Everything sparkles when you're insane! Hee hee!"]},
    "Husk": {"color": 0xFFA500, "gifs": ["https://media.tenor.com/1dF1m1e1X1AAAAAC/husk-hazbin.gif", "https://media.tenor.com/QmX1n1e1X1AAAAAC/husk-hazbin-hotel.gif", "https://media.tenor.com/W1m1e1X1dF1AAAAAC/husk.gif"], "quotes": ["I'm too old for this shit. And I'm literally centuries old.", "The only thing I'm redeeming is my drink.", "Don't talk to me until I've had my first bottle.", "I lost everything because of a deal with Alastor. Don't make deals.", "You want wisdom? Here it is: life sucks, then you die, then it sucks more.", "I used to be an overlord. Now I pour drinks. Hell's hilarious.", "The hotel's doomed. But at least the booze is free.", "I don't believe in redemption. I believe in whiskey."]},
    "Lucifer": {"color": 0xFFD700, "gifs": ["https://media.tenor.com/2dF2m2e2X2AAAAAC/lucifer-hazbin.gif", "https://media.tenor.com/RmX2n2e2X2AAAAAC/lucifer-hazbin-hotel.gif", "https://media.tenor.com/X2m2e2X2dF2AAAAAC/lucifer-morningstar.gif"], "quotes": ["I'm the original fallen angel. You think YOUR problems are bad?", "I created Hell. Well, technically God made the place, I just... furnished it.", "Charlie has more faith in humanity than I ever did. She gets it from her mother.", "Ducks are perfect. I made them. You're welcome.", "I haven't been this disappointed since Eve ate that apple.", "The hotel is a lovely idea. It won't work. But it's lovely.", "I'm not bitter. I'm just... eternally disappointed.", "I could snap my fingers and fix everything. But where's the fun in that?"]},
    "Rosie": {"color": 0xFF69B4, "gifs": ["https://media.tenor.com/3dF3m3e3X3AAAAAC/rosie-hazbin.gif", "https://media.tenor.com/SmX3n3e3X3AAAAAC/rosie-hazbin-hotel.gif", "https://media.tenor.com/Y3m3e3X3dF3AAAAAC/rosie.gif"], "quotes": ["Oh, a fresh face in the colony! How DELIGHTFUL!", "Cannibalism is about community, darling. We all share.", "I've eaten fancier meals than most overlords have eaten souls.", "The hotel is just ADORABLE. I do hope it works out!", "My dear, you look positively delicious today!", "There's nothing a nice chat and a light snack can't solve.", "I've been running this colony for centuries. You learn a thing or two.", "Alastor and I go way back. He's always been such a character!"]},
    "Vox": {"color": 0x00BFFF, "gifs": ["https://media.tenor.com/4dF4m4e4X4AAAAAC/vox-hazbin.gif", "https://media.tenor.com/TmX4n4e4X4AAAAAC/vox-hazbin-hotel.gif"], "quotes": ["I OWN the airwaves in Hell. Everyone else is just background noise.", "Alastor thinks he's relevant. How ADORABLY outdated.", "Television is the future. Radio is a museum piece. Like Alastor.", "I didn't become an overlord by being NICE.", "You want power? Get with the times. Or get out of my way.", "My network reaches every corner of Hell. You're always watching me.", "Valentino and Velvette? They work for ME. Never forget it.", "The V's run Hell now. The rest of you are just living in it."]},
    "Valentino": {"color": 0x8B008B, "gifs": ["https://media.tenor.com/5dF5m5e5X5AAAAAC/valentino-hazbin.gif", "https://media.tenor.com/UmX5n5e5X5AAAAAC/valentino-hazbin-hotel.gif"], "quotes": ["You're ALL my talent. Whether you like it or not.", "Contracts are binding, darling. You signed in blood.", "I made Angel Dust a STAR. He should be THANKING me.", "In my studio, everyone performs. One way or another.", "The V's don't lose. We don't know how.", "Power is about control. And I control everything you see.", "You think you can break a contract with ME? Cute.", "Fashion, fame, fortune -- I own it all. You just rent."]},
    "Velvette": {"color": 0xFF00FF, "gifs": ["https://media.tenor.com/6dF6m6e6X6AAAAAC/velvette-hazbin.gif", "https://media.tenor.com/VmX6n6e6X6AAAAAC/velvette-hazbin-hotel.gif"], "quotes": ["Social media runs Hell now, sweetie. Keep up.", "I'm not just the face of the V's -- I'm the BRAINS.", "One post from me and your reputation is DONE.", "Trends don't happen. I MAKE them happen.", "You're not famous until Velvette says you're famous.", "Outdated? Moi? I'm the only one in Hell with a smartphone.", "I manage the image. Vox handles the tech. Val handles... talent.", "Don't make me cancel you. I mean that literally."]},
    "Carmilla Carmine": {"color": 0xC0C0C0, "gifs": ["https://media.tenor.com/7dF7m7e7X7AAAAAC/carmilla-carmine-hazbin.gif", "https://media.tenor.com/WmX7n7e7X7AAAAAC/carmilla-carmine-hazbin-hotel.gif"], "quotes": ["I built my empire from nothing. What have YOU done?", "The angelic weapons trade keeps Hell running. And I run the trade.", "I have daughters. I know when someone's full of excuses.", "Power isn't given. It's taken. And I took mine.", "I don't make deals with just anyone. You have to prove yourself.", "Angels fall. Weapons don't. Smart investment.", "Zestial is an old friend. We understand each other.", "I've survived every purge. Not by hiding. By fighting."]},
    "Zestial": {"color": 0x2F4F2F, "gifs": ["https://media.tenor.com/8dF8m8e8X8AAAAAC/zestial-hazbin.gif", "https://media.tenor.com/XmX8n8e8X8AAAAAC/zestial-hazbin-hotel.gif"], "quotes": ["I have walked these halls since before many souls were born.", "Patience, young one. Power comes to those who wait.", "I have seen empires rise and fall. The key is to outlast them.", "Carmilla is a dear ally. Her ambition reminds me of myself.", "The old ways are the best ways. Modernity is fleeting.", "I speak in riddles because the truth is too sharp for most.", "An overlord's true strength is not in their power, but in their wisdom.", "Hell changes, but I remain. There is a lesson in that."]},
    "Zeezi": {"color": 0x9370DB, "gifs": ["https://media.tenor.com/9dF9m9e9X9AAAAAC/zeezi-hazbin.gif", "https://media.tenor.com/YmX9n9e9X9AAAAAC/zeezi-hazbin-hotel.gif"], "quotes": ["Being an overlord isn't about power. It's about presence.", "I've been watching Hell's politics for centuries. It's always the same show.", "Rosie and I go way back. Don't believe everything you hear.", "You think you understand Hell? You've barely scratched the surface.", "The balance of power shifts constantly. I simply shift with it.", "I don't need to shout to be heard. That's for amateurs.", "Every overlord has secrets. Mine are just better hidden.", "The game of Hell never ends. You either play or get played."]}
}

CHARACTER_NAMES = list(CHARACTERS.keys())

def make_embed(name):
    ch = CHARACTERS[name]
    q = random.choice(ch["quotes"])
    g = random.choice(ch["gifs"])
    e = discord.Embed(title=f"{name} says...", description=q, color=ch["color"])
    e.set_image(url=g)
    return e

# ───── SLASH COMMANDS ─────

@bot.tree.command(name="quote", description="Get a random quote from a Hazbin Hotel character")
async def slash_quote(interaction: discord.Interaction, character: str = None):
    # Match case-insensitively, supporting multi-word names
    matched = None
    if character:
        for key in CHARACTERS:
            if key.lower() == character.lower():
                matched = key
                break
    if matched:
        name = matched
    elif character and not matched:
        await interaction.response.send_message(f"Character '{character}' not found! Use /characters to see all.", ephemeral=True)
        return
    else:
        name = random.choice(CHARACTER_NAMES)
    e = make_embed(name)
    await interaction.response.send_message(embed=e)

@slash_quote.autocomplete("character")
async def quote_autocomplete(interaction: discord.Interaction, current: str):
    return [
        discord.app_commands.Choice(name=n, value=n)
        for n in CHARACTER_NAMES if current.lower() in n.lower()
    ][:25]

@bot.tree.command(name="characters", description="List all Hazbin Hotel characters available")
async def slash_characters(interaction: discord.Interaction):
    lines = "\n".join([f"• {n}" for n in CHARACTER_NAMES])
    e = discord.Embed(title="🎭 Hazbin Hotel Characters", description=lines, color=0xCC0000)
    await interaction.response.send_message(embed=e)

# ───── DAILY SCHEDULED QUOTE ─────

@tasks.loop(hours=24)
async def daily_quote():
    channel = bot.get_channel(QUOTES_CHANNEL_ID)
    if not channel:
        print(f"Daily quote channel {QUOTES_CHANNEL_ID} not found")
        return
    name = random.choice(CHARACTER_NAMES)
    e = make_embed(name)
    await channel.send(embed=e)
    print(f"Daily quote posted as {name}")

@daily_quote.before_loop
async def before_daily():
    await bot.wait_until_ready()
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc)
    target = QUOTE_TIME.split(":")
    target_hr, target_min = int(target[0]), int(target[1])
    next_run = now.replace(hour=target_hr, minute=target_min, second=0, microsecond=0)
    if next_run <= now:
        next_run += datetime.timedelta(days=1)
    wait = (next_run - now).total_seconds()
    print(f"Daily quote scheduled for {next_run} (in {wait:.0f}s)")
    await asyncio.sleep(wait)

# ───── STARTUP ─────

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    print("Slash commands synced!")
    daily_quote.start()

import asyncio
bot.run(DISCORD_TOKEN)