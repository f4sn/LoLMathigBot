import discord

db = {}
emojiId = {
    "top": 698499096301797409,
    "mid": 698499096444403775,
    "jg": 698499096645861426,
    "sup": 698499096624889927,
    "adc": 698499096624889916,
    "check": 698500655286976565
    }
battleLock = False
with open('./token.txt') as tokenFile:
    tokenStr = tokenFile.readline().rstrip()


with open('./db') as dbfile:
    line = dbfile.readline()
    while line:
        dbObject = line.split()
        db[dbObject[0]] = dbObject[1]
        line = dbfile.readline()

client = discord.Client()

def addDb(id, rate):
    with open('./db', mode='a') as dbfile:
        dbfile.write(f"{id} {rate}\n")

def updateDb():
    with open('./db') as dbfile:
        line = dbfile.readline()
        while line:
            dbObject = line.split()
            db[dbObject[0]] = dbObject[1]
            line = dbfile.readline()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    
    if message.content.startswith("!rate") or message.content.startswith("!rank"):
        if client.user != message.author:
            args = message.content.split()
            addDb(message.author.discriminator, args[1])
            m = f"{message.author.name}のレートを更新しました。"
            await message.channel.send(m)

            
    if message.content.startswith("!紅白"):
        if client.user != message.author:
            if battleLock:
                m = "現在別の紅白戦が進行中です。"
            else:
                m = "行きたいレーンを押してください。\n押し終わったらチェックマークを押してください。"
                updateDb()
            await message.channel.send(m)
    
    if message.content.startswith("行きたい") and client.user == message.author:
        await message.add_reaction(client.get_emoji(emojiId["top"]))
        await message.add_reaction(client.get_emoji(emojiId["jg"]))
        await message.add_reaction(client.get_emoji(emojiId["mid"]))
        await message.add_reaction(client.get_emoji(emojiId["sup"]))
        await message.add_reaction(client.get_emoji(emojiId["adc"]))
        await message.add_reaction(client.get_emoji(emojiId["check"]))

#ここやる
@client.event
async def on_reaction_add(reaction, user):
    print("emoji-id")
    print(reaction.emoji.id)

client.run(tokenStr)

#TODO アカウントのロック
#レートない人の対応
#共演
#計算の移行
#リアクション対応してない