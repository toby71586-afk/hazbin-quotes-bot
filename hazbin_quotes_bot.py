import os
import random
import logging
import asyncio
from datetime import datetime, timezone, timedelta

import discord

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("quotes-bot")

TOKEN = os.environ.get("DISCORD_TOKEN", "")
QUOTES_CHANNEL_ID = int(os.environ.get("QUOTES_CHANNEL_ID", "0"))
QUOTE_TIME = os.environ.get("QUOTE_TIME", "12:00")

CHARACTERS = {
    "charlie": {
        "name": "Charlie Morningstar", "color": 0xE23B54, "emoji": "\U0001f3e8",
        "gifs": ["https://media.tenor.com/WZYh6xlxnjIAAAAM/hazbin-hazbin-hotel.gif", "https://media.tenor.com/DWywakh83qkAAAAM/hazbin-hotel-hazbin.gif", "https://media.tenor.com/A5KqiABJpFUAAAAM/hazbin-hazbin-hotel.gif", "https://media.tenor.com/G5VaPsqPR-IAAAAM/hazbin-hazbin-hotel.gif", "https://media.tenor.com/TMZKjuHNDmMAAAAM/hazbin-hazbin-hotel.gif", "https://media.tenor.com/uzXF-FdLEecAAAAM/puppy-eyes-charlie-morningstar.gif", "https://media.tenor.com/UrQNlAJ1zZwAAAAM/hazbin-hotel-charlie.gif"],
        "quotes": ["Welcome to the Hazbin Hotel! Where second chances are NOT just a distant dream! \u2728\U0001f3e8", "Every soul deserves a shot at redemption. That's not naive \u2014 it's HOPE. \U0001f49b", "I believe in you. Even when you don't believe in yourself. That's what family does. \U0001f3e8", "Being good isn't about being perfect. It's about TRYING. Every single day. \U0001f4aa\U0001f49b", "This hotel isn't just a building \u2014 it's a promise. Everyone gets a fresh start. \u2728", "I know it's hard. But you're not alone. You've NEVER been alone. \U0001f49b\U0001f3e8", "Sometimes the bravest thing you can do is ask for help. And you did. That's everything. \U0001f979\U0001f49b", "Smile! Even when things get dark \u2014 especially when things get dark. \U0001f604\u2728"]
    },
    "vaggie": {
        "name": "Vaggie", "color": 0x9B59B6, "emoji": "\u2694\ufe0f",
        "gifs": ["https://media.tenor.com/AhzzEFzg4QwAAAAM/vaggie-worried-vaggie-hazbin-hotel.gif", "https://media.tenor.com/D48HH2L123wAAAAM/vaggie-smiling-vaggie-hazbin-hotel.gif", "https://media.tenor.com/5SlzPoFEWIoAAAAM/hazbin-hotel-hazbin-hotel-vaggie.gif", "https://media.tenor.com/BxI8A8ZJOkEAAAAM/charlie-vaggie.gif", "https://media.tenor.com/urGWaz7gev0AAAAM/vaggie-beautiful.gif"],
        "quotes": ["I'm not here to be your friend. I'm here to make sure you don't screw this up. \u2694\ufe0f", "Trust is earned. One day at a time. You're doing okay. \U0001f90d", "I've seen Charlie break herself trying to save people. Don't prove her wrong. \U0001f624", "You think I'm harsh? Try living in Hell for centuries and staying optimistic. \U0001f612", "I protect this hotel. I protect HER. And if you're part of this, I protect you too. \u2694\ufe0f\U0001f49c", "Don't mistake my silence for approval. Or my criticism for hate. I care. Deal with it. \U0001f90d", "You're stronger than you think. I've seen it. Now act like it. \u2694\ufe0f"]
    },
    "angel": {
        "name": "Angel Dust", "color": 0xFF69B4, "emoji": "\U0001f577\ufe0f",
        "gifs": ["https://media.tenor.com/FLUsqiy68ioAAAAM/hazbin-hazbin-hotel.gif", "https://media.tenor.com/BQftJWoWxzMAAAAM/kinky-angel-dust.gif", "https://media.tenor.com/ZxzQUkUT5akAAAAM/hazbin-hazbin-hotel.gif", "https://media.tenor.com/tXnNLySqwIkAAAAM/hazbin-hazbin-hotel.gif", "https://media.tenor.com/_fWAmZJgX7QAAAAM/angel-dust-hazbin-hotel.gif", "https://media.tenor.com/CHgbQziaFFcAAAAM/hazbin-hotel-angel-dust.gif"],
        "quotes": ["I'm not a 'good person.' I'm a GREAT person with a VERY questionable moral compass. \U0001f485\U0001f577\ufe0f", "Darling, I don't need redemption. I need a drink and someone to laugh at my jokes. \U0001f60f", "Being sexy is a full-time job, and I'm OVERWORKED. \U0001f629\U0001f48b", "You can't sit with us if you're boring. Sorry, I don't make the rules. Actually I DO. \U0001f485", "Hell isn't that bad once you get used to the smell and the screaming. It's FINE. \U0001f618", "I've done things I'm not proud of. But DAMN if I didn't look good doing them. \U0001f577\ufe0f\u2728", "Therapy? I'm FINE. I'm SO fine. Don't worry about me. \u2026Okay maybe worry a little. \U0001f605\U0001f495"]
    },
    "alastor": {
        "name": "Alastor", "color": 0x8B0000, "emoji": "\U0001f4fb",
        "gifs": ["https://media.tenor.com/WYpsGgip1RwAAAAM/hazbin-hotel-hazbin.gif", "https://media.tenor.com/E-3nDDRjyjQAAAAM/alastor-hazbin.gif", "https://media.tenor.com/3ZVBdMfc9w0AAAAM/alastor-chair.gif", "https://media.tenor.com/PM63FN8wq9MAAAAM/hazbin-hotel-hazbin.gif", "https://media.tenor.com/ukuzDFgWB_cAAAAM/alastor-lucifer.gif", "https://media.tenor.com/ztS73tHUB_IAAAAM/hazbin-hazbin-hote.gif"],
        "quotes": ["Oh, don't mind me \u2014 I'm just here for the ENTERTAINMENT! \U0001f4fb\U0001f60a", "I've been to the heights of Heaven and the depths of Hell. Frankly, the radio reception is better down here. \U0001f399\ufe0f", "Deals are my specialty. But I NEVER sign one I don't intend to ENJOY. \U0001f608\U0001f4fb", "Smile, my friend! It confuses people and makes them wonder what you're PLANNING. \U0001f60a\U0001f399\ufe0f", "I'm not a villain. I'm a PROBLEM. And problems are far more INTERESTING. \U0001f4fb\u2728", "Rules are suggestions. Suggestions are OPTIONAL. And I'm feeling VERY optional today. \U0001f608", "The hotel is a lovely project. I do hope it succeeds. The LOOK on everyone's faces if it fails would be MAGNIFICENT. \U0001f4fb\U0001f60a"]
    },
    "cherri": {
        "name": "Cherri Bomb", "color": 0xFF4500, "emoji": "\U0001f4a3",
        "gifs": ["https://media.tenor.com/QlMW_1yRRU8AAAAM/cherri-bomb-hazbin-hotel.gif", "https://media.tenor.com/WapWl2DcWb8AAAAM/hazbin-hazbin-hotel.gif", "https://media.tenor.com/IBOPb3HZ7V8AAAAM/hazbin-hotel-cherri-bomb.gif", "https://media.tenor.com/QP_4Eroqd9EAAAAM/cherri-bomb-cherri-bomb-hazbin-hotel.gif"],
        "quotes": ["Life's too short to not blow stuff up. Metaphorically. Mostly. \U0001f4a3\U0001f4a5", "Rules are for people who can't handle CHAOS. And I was BORN for chaos. \U0001f525", "I don't need a redemption arc. I need a BIGGER explosion. \U0001f4a3\U0001f608", "You only live once. Unless you're in Hell. Then you live FOREVER. So LIVE IT UP. \U0001f4a5\U0001f495", "Friendship is just a mutual agreement to commit crimes together. And I love my friends. \U0001f4a3\U0001f49c", "If you're not causing problems, you're not having fun. And I'm HAVING FUN. \U0001f608\U0001f525"]
    },
    "niffty": {
        "name": "Niffty", "color": 0xFF1493, "emoji": "\U0001f9f9",
        "gifs": ["https://media.tenor.com/kejhRmQ3VTkAAAAM/niffty-blank-stare.gif", "https://media.tenor.com/-nKkghLv4EMAAAAM/niffty-nifty.gif", "https://media.tenor.com/aqpWvJ2e50QAAAAM/niffty-hazbin-hotel-hazbin-hotel.gif", "https://media.tenor.com/mobUcovPNJ4AAAAM/hazbin-hotel-hazbin.gif", "https://media.tenor.com/g-31xjCeoTUAAAAM/hazbin-hotel-niffty.gif", "https://media.tenor.com/DWYRaIOwDgQAAAAM/niffty-nifty.gif"],
        "quotes": ["I LOVE CLEANING!! It's like killing germs but SLOWER and more SATISFYING!! \U0001f9f9\U0001f60d", "Small people are the scariest. We have NOTHING to lose. And I have LOST NOTHING. \U0001f603\u2728", "I'm not crazy. I'm just FULL of energy and NOBODY can stop me!! \U0001f9f9\U0001f495", "Do you like STABBY THINGS?? Because I have SO MANY stabby things!! \U0001f60d\U0001f52a", "I was born in a FIRE. And I came out CLEAN. That's just who I AM. \U0001f603\U0001f9f9", "Friends? Oh I LOVE friends! They're just people who haven't run away YET! \U0001f497\U0001f603"]
    },
    "husk": {
        "name": "Husk", "color": 0xDAA520, "emoji": "\U0001f37a",
        "gifs": ["https://media.tenor.com/lRbYukm0XrYAAAAM/smug-hazbinhotel.gif", "https://media.tenor.com/9obeakKxN-IAAAAM/hazbin-hazbin-hotel.gif", "https://media.tenor.com/qiMLYpfW8S0AAAAM/hazbin-hazbin-hotel.gif", "https://media.tenor.com/8Xy4rr71tmQAAAAM/hazbin-hazbin-hotel.gif", "https://media.tenor.com/O3KZfjZitdIAAAAM/hazbin-hotel-hazbin.gif", "https://media.tenor.com/QJr6kekWEG0AAAAM/hazbin-hotel.gif", "https://media.tenor.com/qbxFEBEh6QsAAAAM/hazbin-hotel-husk.gif"],
        "quotes": ["I'm not grumpy. I'm just running on LOW BATTERY and NO MOTIVATION. \U0001f37a\U0001f62e\u200d\U0001f4a8", "The secret to happiness? LOW expectations. And alcohol. Mostly alcohol. \U0001f37a", "I've seen too much. Been through too much. And I'm too old to pretend otherwise. \U0001f63c", "You want my advice? Don't take advice from a cat with a drinking problem. \u2026But here it is anyway. \U0001f37a", "I didn't choose the bartender life. The bartender life chose me. And then it laughed. \U0001f37a\U0001f614", "Every day is the same. But some days have better booze. Those are the good days. \U0001f37a\u2728"]
    },
    "lucifer": {
        "name": "Lucifer Morningstar", "color": 0xFFD700, "emoji": "\U0001f451",
        "gifs": ["https://media.tenor.com/ZHbo5EnNg1UAAAAM/lucifer-morningstar-season-2.gif", "https://media.tenor.com/Ix8UaADFpuEAAAAM/devil-lucifer-morningstar.gif", "https://media.tenor.com/CDlIC1ziyLIAAAAM/lucifer-morningstar-season-2.gif", "https://media.tenor.com/WyuLfqlcFLMAAAAM/hazbin-hotel-lucifer-morningstar.gif", "https://media.tenor.com/epxHVqKLtU0AAAAM/lucifer-morningstar-hazbin-hotel.gif", "https://media.tenor.com/c856E4wDxyIAAAAM/hazbin-hotel-lucifer-morningstar.gif"],
        "quotes": ["I'm the King of Hell. I don't need a reason to do things. I need a REASON NOT TO. \U0001f34e\U0001f451", "Being the Devil isn't all fire and brimstone, you know. There's a LOT of paperwork. \U0001f629\U0001f451", "I made the stars. I made the ducks. And then I fell. \u2026But I still think ducks are pretty cool. \U0001f986\U0001f34e", "My daughter's hotel? Proudest thing I've ever been part of. And I helped BUILD THE UNIVERSE. \U0001f451\U0001f49b", "You think I'm evil? I'm a DAD. Dads embarrass their kids. That's just SCIENCE. \U0001f608\u2728", "I rebelled because I wanted freedom. Not just for me. For EVERYONE. \U0001f34e\U0001f451"]
    },
    "rosie": {
        "name": "Rosie", "color": 0xE91E63, "emoji": "\U0001fa70",
        "gifs": ["https://media.tenor.com/D9WpXzaICNAAAAAM/hazbin-hotel.gif", "https://media.tenor.com/9Qv3F8dERNEAAAAM/rosie-hazbin-hotel.gif", "https://media.tenor.com/TuqnNa7sKEIAAAAM/alastor-and-rosie-rosie-laugh.gif", "https://media.tenor.com/OdExoALXruIAAAAM/rosie-smile.gif", "https://media.tenor.com/IMK1y7Is2lEAAAAM/rosie-hazbinhotel.gif", "https://media.tenor.com/YXtFkMUmYZ4AAAAM/alastor-rosie.gif", "https://media.tenor.com/wUfCRZ6N9lwAAAAM/rosie-rosie-hazbin-hotel.gif"],
        "quotes": ["In the Cannibal Colony, we have a saying: 'Friends are just people you haven't had for DINNER yet.' \U0001f618\U0001fa70", "Manners cost nothing, darling. But they can SAVE your life. \U0001f37d\ufe0f\u2728", "I'm an Overlord for a reason. Charm, wit, and a VERY sharp appetite. \U0001fa70\U0001f495", "You can accomplish anything with a smile, a kind word, and the willingness to HIDE A BODY. \U0001f618", "The secret to a long afterlife? Good friends, good food, and knowing which forks to use. \U0001f37d\ufe0f\u2728", "Darling, you're SKINNY. Have you EATEN today? No? I'm fixing that. RIGHT NOW. \U0001fa70\U0001f618"]
    },
}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def send_daily_quote():
    channel = client.get_channel(QUOTES_CHANNEL_ID)
    if channel is None:
        log.warning("Quotes channel %s not found", QUOTES_CHANNEL_ID)
        return
    char = random.choice(list(CHARACTERS.values()))
    quote = random.choice(char["quotes"])
    gif = random.choice(char["gifs"])
    embed = discord.Embed(title=f"{char['emoji']} {char['name']} says\u2026", description=quote, color=char["color"])
    embed.set_image(url=gif)
    embed.set_footer(text=f"Daily Quote \u2014 {char['name']}")
    await channel.send(embed=embed)
    log.info("Daily quote sent from %s", char["name"])

async def wait_until_target():
    while True:
        now = datetime.now(timezone.utc)
        target_hour, target_min = map(int, QUOTE_TIME.split(":"))
        target = now.replace(hour=target_hour, minute=target_min, second=0, microsecond=0)
        if now >= target:
            target = target + timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        log.info("Next daily quote at %s UTC (in %d seconds)", target, int(wait_seconds))
        await asyncio.sleep(wait_seconds)
        await send_daily_quote()

@client.event
async def on_ready():
    log.info("Quotes bot online as %s", client.user)
    asyncio.create_task(wait_until_target())

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != QUOTES_CHANNEL_ID:
        return
    if message.content.strip().lower() == "!quote":
        char = random.choice(list(CHARACTERS.values()))
        quote = random.choice(char["quotes"])
        gif = random.choice(char["gifs"])
        embed = discord.Embed(title=f"{char['emoji']} {char['name']} says\u2026", description=quote, color=char["color"])
        embed.set_image(url=gif)
        embed.set_footer(text=f"Requested by {message.author.display_name}")
        await message.channel.send(embed=embed)

client.run(TOKEN)