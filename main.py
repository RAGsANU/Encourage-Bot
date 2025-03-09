import discord
import os
import requests
import json
import random
from replit import db

# Enable all required intents
intents = discord.Intents.default()
intents.message_content = True  # Explicitly enable message content intent

client = discord.Client(intents=intents)

db_url = os.environ['REPLIT_DB_URL']
print("Connected to:", db_url)

sad_words =["sad","depressed","unhappy","angry","miserable","depressing"]

starter_encuoragements = [
    "cheer up !",
    "hang in there",
    "you are a great person /bot !"
]

if "responding"not in db.keys():
    db["responding"] =True

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" +json_data[0]['a']
    return (quote)

def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements

    else:
        db["encouragements"] = [encouraging_message]

    def delete_encouragement(index):
        ecouragements = db["encouragements"]
        if len(encouragements) >index:
            del encouragements[index]
            db["encouragements"] = encouragements

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"Received message: '{message.content}' from {message.author}")  # Debugging

    msg = message.content

    if message.content.strip() == "$inspire":
        print("Bot detected $hello command!") # Debugging
        quote = get_quote()
        await message.channel.send(quote)

    if message.content.strip() == "$hello":
        await message.channel.send("Hello! how are you doin ?")
    
    if db["responding"]:
        options = starter_encuoragements
        if "encouragements" in db.keys():
            options = options + list(db["encouragements"])


        if any(word in msg for word in sad_words) :
            await message.channel.send(random.choice (options))

    if msg.startswith("$new"):
        encouraging_message = msg.split("new ",1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("new encouraging message added !")    

    if msg.startswith("$del"):
        if "encouragements" in db.keys():
            encouragements = list(db["encouragements"])
            index = int(msg.split("$del ", 1)[1])

        # Handle out-of-range error
        if index < len(encouragements):
            deleted_message = encouragements.pop(index)
            db["encouragements"] = encouragements
            await message.channel.send(f"✅ Deleted: '{deleted_message}'")
        else:
            await message.channel.send("⚠️ Index out of range! Try again.")

        # Send all remaining encouragements
        if len(encouragements) > 0:
            await message.channel.send("🎉 Remaining Encouragements:")
            for i, msg in enumerate(encouragements):
                await message.channel.send(f"{i}. {msg}")
        else:
            await message.channel.send("💀 No encouragement messages left!")

    if msg.startswith("$list"):
        encouragements =[]
        if "encouragements" in db.keys():
            encouragements = list(db["encouragements"])
            await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value =msg.split("$responding ",1)[1]

        if value.lower() == "true":
            db ["responding"] = True
            await message.channel.send("responding is on. ")
        if value.lower() == "true":
            db ["responding"] = False
            await message.channel.send("responding is off. ")

client.run(os.getenv('TOKEN'))
