import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

greeting_msg = ["Yo!", "Howdy!", "Hola!", "Hey wassup!"]

sad_words = ["sad", "frustrated", "depressed", "unhappy", "miserable", "depressing", "angry", "heartbroken", "grief", "down"]

starter_encouragements = [
  "Cheer up!, I am there for you!",
  "Just listen to some uplifting songs, you will be fine", 
  "Dont worry buddy, life is a mixture of ups and downs",
  "You are a great person"
]

if "#responding" not in db.keys():
  db["#responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' - ' + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    global starter_encouragements
    starter_encouragements.append(encouraging_message)
    db["encouragements"] = starter_encouragements

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return 

  msg = message.content

  if msg.startswith('#hello'):
    await message.channel.send(random.choice(greeting_msg))

  if msg.startswith('#motivate'):
    quote = get_quote()
    await message.channel.send(quote)


  if db["#responding"]:  
    options = starter_encouragements

    if "encouragements" in db.keys():
      options += db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))


  # the new msgs gets appended in 'starter_encouragements' list
  if msg.startswith("#new"):
    new_enc_message = msg.split("#new ", 1)[1]
    update_encouragements(new_enc_message)
    await message.channel.send("New encouraging message added!")

  if msg.startswith("#list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      if len(encouragements) == 0:
        await message.channel.send('The list is empty please add new encouragements by command "#new"')
      else:
        await message.channel.send(encouragements.value)

  if msg.startswith("#del"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      if len(encouragements) == 0:
        await message.channel.send('The list is empty please add new encouragements by command "#new"')
      else:
        index = int(msg.split("#del", 1)[1])
        delete_encouragement(index)
        await message.channel.send("The encouraging message is deleted!")

  if msg.startswith("#responding"):
    value = msg.split("#responding ", 1)[1]

    if value.lower() == "true":
      db["#responding"] = True
      await message.channel.send("I will be responding to sad messages.")
    else:
      db["#responding"] = False
      await message.channel.send("I will be no longer responding to sad messages.")


keep_alive()
my_secret = os.environ['TOKEN']
client.run(os.getenv('TOKEN'))
